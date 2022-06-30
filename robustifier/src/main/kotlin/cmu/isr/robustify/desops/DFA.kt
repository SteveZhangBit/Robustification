package cmu.isr.robustify.desops

import net.automatalib.automata.fsa.DFA
import net.automatalib.automata.fsa.impl.compact.CompactDFA

interface SupervisoryDFA<S, I> : DFA<S, I> {

  val controllable: Collection<I>

  val observable: Collection<I>

}


class CompactSupDFA<I>(
  dfa: CompactDFA<I>,
  override val controllable: Collection<I>,
  override val observable: Collection<I>
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


fun <I> CompactDFA<I>.asSupDFA(controllable: Collection<I>, observable: Collection<I>): CompactSupDFA<I> {
  return CompactSupDFA(this, controllable, observable)
}
