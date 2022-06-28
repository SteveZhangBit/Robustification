package cmu.isr.robustify

import cmu.isr.lts.DetLTS


/**
 * @param sys The LTS of the system specification.
 * @param devEnv The deviated environment.
 * @param safety The LTS of the safety property. It does not need to be complete.
 */
abstract class BaseRobustifier<S, I, T>(
  val sys: DetLTS<S, I, T>,
  val devEnv: DetLTS<S, I, T>,
  val safety: DetLTS<S, I, T>
) {

  /**
   * Synthesize a new system model such that it satisfies the safety property under the deviated environment.
   */
  abstract fun synthesize(): DetLTS<S, I, T>?
}
