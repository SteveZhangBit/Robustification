package cmu.isr.robustify.desops

import net.automatalib.automata.fsa.DFA
import net.automatalib.automata.fsa.impl.compact.CompactDFA
import net.automatalib.words.Alphabet

interface SupervisoryDFA<S, I> : DFA<S, I> {

  val controllable: Alphabet<I>

  val observable: Alphabet<I>

}


class CompactSupDFA<I>(
  dfa: CompactDFA<I>,
  override val controllable: Alphabet<I>,
  override val observable: Alphabet<I>
) : CompactDFA<I>(dfa), SupervisoryDFA<Int, I> {

  override fun getSuccessor(transition: Int?): Int {
    return super<CompactDFA>.getSuccessor(transition)
  }

  override fun getStateProperty(state: Int?): Boolean {
    return super<CompactDFA>.getStateProperty(state)
  }

  override fun getTransitionProperty(transition: Int?): Void? {
    return super<CompactDFA>.getTransitionProperty(transition)
  }

}


fun <I> CompactDFA<I>.asSupDFA(controllable: Alphabet<I>, observable: Alphabet<I>): CompactSupDFA<I> {
  return CompactSupDFA(this, controllable, observable)
}
