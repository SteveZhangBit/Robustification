package cmu.isr.robustify.supervisory

import cmu.isr.lts.DetLTS
import cmu.isr.robustify.BaseRobustifier
import cmu.isr.robustify.desops.CompactSupDFA
import cmu.isr.robustify.desops.DESopsRunner
import cmu.isr.robustify.desops.asSupDFA
import net.automatalib.automata.fsa.impl.compact.CompactDFA
import net.automatalib.words.Alphabet
import net.automatalib.words.Word
import org.slf4j.LoggerFactory
import cmu.isr.lts.parallelComposition as parallelLTS
import cmu.isr.robustify.desops.parallelComposition as parallelDFA

enum class Priority { P0, P1, P2, P3 }

enum class Algorithms { Pareto, Fast }

class WeightsMap<I>(val preferred: Map<Word<I>, Int>, val controllable: Map<I, Int>, val observable: Map<I, Int>)


class SupervisoryRobustifier<S, T>(
  sys: DetLTS<S, String, T>,
  sysInputs: Alphabet<String>,
  devEnv: DetLTS<S, String, T>,
  envInputs: Alphabet<String>,
  safety: DetLTS<S, String, T>,
  safetyInputs: Alphabet<String>,
  progress: Collection<String>,
  private val preferredMap: Map<Priority, Collection<Word<String>>>,
  private val controllableMap: Map<Priority, Collection<String>>,
  private val observableMap: Map<Priority, Collection<String>>,
) : BaseRobustifier<S, String, T>(sys, devEnv, safety)
{
  private val logger = LoggerFactory.getLogger(javaClass)
  private val desops = DESopsRunner()
  private val plant = parallelLTS(sys, sysInputs, devEnv, envInputs)
  private val inputs = plant.inputAlphabet
  private val prop: CompactDFA<String>

  init {
    val extendedSafety = extendAlphabet(safety, safetyInputs, inputs)
    val progressProp = progress.map { makeProgress(it) }
    var c = extendedSafety as CompactDFA<String>
    for (p in progressProp) {
      c = parallelDFA(c, c.inputAlphabet, p, p.inputAlphabet)
    }
    prop = c
  }

  override fun synthesize(): DetLTS<S, String, T>? {
    return synthesize(Algorithms.Pareto).firstOrNull()
  }

  fun synthesize(alg: Algorithms, deadlockFree: Boolean = false): SolutionIterator<S, String, T> {
    logger.info("==============================>")
    logger.info("Initializing search by using $alg search...")

    // flatten the preferred behaviors
    val preferred = preferredMap.flatMap { it.value }
    logger.info("Number of preferred behaviors: ${preferred.size}")

    // compute weight map
    val weights = computeWeights()
    // get controllable and observable events
    val controllable = weights.controllable.keys
    val observable = weights.observable.keys
    logger.info("Number of controllable events with cost: ${controllable.size}")
    logger.info("Number of observable events with cost: ${observable.size}")

    val sup = synthesize(controllable, observable)

    return SolutionIterator()
  }

  private fun synthesize(controllable: Collection<String>, observable: Collection<String>): CompactSupDFA<String>? {
    val g = plant.asSupDFA(controllable, observable)
    val p = prop.asSupDFA(controllable, observable)
    return desops.synthesize(g, g.inputAlphabet, p, p.inputAlphabet)
  }

  /**
   * Given the priority ranking that the user provides, compute the positive utilities for preferred behavior
   * and the negative cost for making certain events controllable and/or observable.
   * @return dictionary with this information.
   */
  private fun computeWeights(): WeightsMap<String> {
    val preferred = mutableMapOf<Word<String>, Int>()
    val controllable = mutableMapOf<String, Int>()
    val observable = mutableMapOf<String, Int>()

    var totalWeight = 0
    // compute new weight in order to maintain hierarchy by sorting absolute value sum of previous weights
    for (p in listOf(Priority.P1, Priority.P2, Priority.P3)) {
      val curWeight = totalWeight + 1
      if (p in preferredMap) {
        for (word in preferredMap[p]!!) {
          preferred[word] = curWeight
          totalWeight += curWeight
        }
      }
      if (p in controllableMap) {
        for (a in controllableMap[p]!!) {
          controllable[a] = -curWeight
          totalWeight += curWeight
        }
      }
      if (p in observableMap) {
        for (a in observableMap[p]!!) {
          observable[a] = -curWeight
          totalWeight += curWeight
        }
      }
    }

    return WeightsMap(preferred, controllable, observable)
  }

}