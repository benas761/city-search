import customerRules
import searchAlgorithms

searchMap = {
    'brute': searchAlgorithms.brute,
    'random': searchAlgorithms.random,
    'rdoa': searchAlgorithms.rdoa,
    'rdoa-d': searchAlgorithms.rdoa_d
  }
objectiveMap = {
  'binary': customerRules.binary.binary,
  'proportional': customerRules.proportional.proportional,
  'partiallyProportional': customerRules.proportional.partiallyProportional,
  'paretoProportional': customerRules.proportional.paretoProportional
}