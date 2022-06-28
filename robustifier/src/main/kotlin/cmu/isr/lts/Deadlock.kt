package cmu.isr.lts

import net.automatalib.commons.util.Holder
import net.automatalib.util.ts.traversal.TSTraversal
import net.automatalib.util.ts.traversal.TSTraversalAction
import net.automatalib.util.ts.traversal.TSTraversalVisitor
import net.automatalib.words.Alphabet


class DeadlockResult<I> {
  var violation: Boolean = false
  var trace: List<I>? = null

  override fun toString(): String {
    return if (violation) "Found deadlock: $trace" else "No deadlock"
  }
}


private class DeadlockVisitor<S, I, T>(private val lts: DetLTS<S, I, T>,
                                       private val inputs: Alphabet<I>,
                                       private val result: DeadlockResult<I>) : TSTraversalVisitor<S, I, T, List<I>> {
  private val visited = mutableSetOf<S>()

  override fun processInitial(state: S, outData: Holder<List<I>>?): TSTraversalAction {
    outData!!.value = emptyList()
    return TSTraversalAction.EXPLORE
  }

  override fun startExploration(state: S, data: List<I>?): Boolean {
    return if (state !in visited) {
      visited.add(state)
      true
    } else {
      false
    }
  }

  override fun processTransition(
    source: S,
    srcData: List<I>?,
    input: I,
    transition: T,
    succ: S,
    outData: Holder<List<I>>?
  ): TSTraversalAction {
    outData!!.value = srcData!! + listOf(input)
    if (!lts.isErrorState(succ) && noOutputTransition(succ)) {
      result.violation = true
      result.trace = outData.value
      return TSTraversalAction.ABORT_TRAVERSAL
    }
    return TSTraversalAction.EXPLORE
  }

  private fun noOutputTransition(state: S): Boolean {
    val res = true
    for (a in inputs) {
      if (lts.getTransition(state, a) != null)
        return false
    }
    return res
  }

}


/**
 * Check the deadlock of a given LTS.
 */
fun <S, I, T> checkDeadlock(lts: DetLTS<S, I, T>, inputs: Alphabet<I>): DeadlockResult<I>
{
  val result = DeadlockResult<I>()
  val vis = DeadlockVisitor(lts, inputs, result)
  TSTraversal.breadthFirst(lts, inputs, vis)
  return result
}
