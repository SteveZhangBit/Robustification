package cmu.isr.robustify.desops

import net.automatalib.util.automata.builders.AutomatonBuilders
import net.automatalib.words.Alphabet
import net.automatalib.words.impl.Alphabets
import java.io.FileOutputStream


class DESopsRunner {

  private val desops = ClassLoader.getSystemResource("scripts/desops.py")?.readBytes() ?: error("Cannot find desops.py")

  init {
    val out = FileOutputStream("./desops.py")
    out.write(desops)
    out.close()
  }

  fun <I> synthesize(plant: SupervisoryDFA<*, I>, inputs1: Alphabet<I>,
                     prop: SupervisoryDFA<*, I>, inputs2: Alphabet<I>): CompactSupDFA<String>? {
    val processBuilder = ProcessBuilder("python", "desops.py")
    val process = processBuilder.start()

    write(process.outputStream, plant, inputs1)
    write(process.outputStream, prop, inputs2)
    process.waitFor()
    return when (process.exitValue()) {
      0 -> parse(process.inputStream)
      1 -> null
      else -> throw Error(process.errorStream.readBytes().toString())
    }
  }

}


fun main() {
  val inputs = Alphabets.fromArray('a', 'b', 'c')
  val controllable = Alphabets.fromArray('a', 'b', 'c')
  val observable = Alphabets.fromArray('a', 'b', 'c')
  val a = AutomatonBuilders.newDFA(inputs)
    .withInitial(0)
    .from(0).on('a').to(1)
    .from(1)
    .on('a').to(1)
    .on('b').to(2)
    .from(2).on('c').to(0)
    .withAccepting(0, 1, 2)
    .create()
    .asSupDFA(controllable, observable)

  val b = AutomatonBuilders.newDFA(inputs)
    .withInitial(0)
    .from(0).on('a').to(1)
    .from(1).on('b').to(2)
    .from(2).on('c').to(0)
    .withAccepting(0, 1, 2)
    .create()
    .asSupDFA(controllable, observable)

  val runner = DESopsRunner()
  val controller = runner.synthesize(a, inputs, b, inputs)

  if (controller != null)
    write(System.out, controller, controller.inputAlphabet)
}