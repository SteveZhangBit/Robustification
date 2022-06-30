package cmu.isr.robustify.supervisory

import cmu.isr.lts.DetLTS
import org.slf4j.LoggerFactory

class SolutionIterator<S, I, T>(

) : Iterable<DetLTS<S, I, T>> {

  private val logger = LoggerFactory.getLogger(javaClass)

  override fun iterator(): Iterator<DetLTS<S, I, T>> {
    TODO("Not yet implemented")
  }

}