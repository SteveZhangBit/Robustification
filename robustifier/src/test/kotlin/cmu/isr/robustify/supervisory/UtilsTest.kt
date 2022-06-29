package cmu.isr.robustify.supervisory

import cmu.isr.lts.asLTS
import cmu.isr.robustify.desops.parallelComposition
import net.automatalib.util.automata.Automata
import net.automatalib.util.automata.builders.AutomatonBuilders
import net.automatalib.words.impl.Alphabets
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class UtilsTest {

  @Test
  fun testExtendAlphabet() {
    val a = AutomatonBuilders.newDFA(Alphabets.fromArray('a', 'b'))
      .withInitial(0)
      .from(0).on('a').to(1)
      .from(1).on('b').to(0)
      .withAccepting(0, 1)
      .create()
      .asLTS()
    val inputs = Alphabets.fromArray('a', 'b', 'c')

    val extended = extendAlphabet(a, a.inputAlphabet, inputs)
    assertEquals(inputs, extended.inputAlphabet)

    val b = AutomatonBuilders.newDFA(Alphabets.fromArray('a', 'b', 'c'))
      .withInitial(0)
      .from(0).on('a').to(1).on('c').to(0)
      .from(1).on('b').to(0).on('c').to(1)
      .withAccepting(0, 1)
      .create()
      .asLTS()

    assert(Automata.testEquivalence(extended, b, inputs)) { println(Automata.findSeparatingWord(extended, b, inputs)) }
  }

  @Test
  fun testParallelComposition() {
    val a = AutomatonBuilders.newDFA(Alphabets.fromArray('a', 'b'))
      .withInitial(0)
      .from(0).on('a').to(1)
      .from(1).on('b').to(0)
      .withAccepting(0, 1)
      .create()

    val b = AutomatonBuilders.newDFA(Alphabets.fromArray('c'))
      .withInitial(0)
      .from(0).on('c').to(1)
      .from(1).on('c').to(1)
      .withAccepting(1)
      .create()

    val c = parallelComposition(a, a.inputAlphabet, b, b.inputAlphabet)

    val d = AutomatonBuilders.newDFA(Alphabets.fromArray('a', 'b', 'c'))
      .withInitial(0)
      .from(0).on('c').to(1).on('a').to(3)
      .from(1).on('c').to(1).on('a').to(2)
      .from(2).on('c').to(2).on('b').to(1)
      .from(3).on('c').to(2).on('b').to(0)
      .withAccepting(1, 2)
      .create()

    assertEquals(Alphabets.fromArray('a', 'b', 'c'), c.inputAlphabet)
    assert(Automata.testEquivalence(c, d, d.inputAlphabet))
  }
}