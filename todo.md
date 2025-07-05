- create a JsonFileExporter
  - split a mixin maybe, have the same structure of classes/function than string exporter
+ check if we can export NAGs as chars instead of ints; maybe both
+ formatted or concise json as option (edn only does concise)
= flush/reset under the hood nicely
+ check if we can export board images into the json/edn
  - at variations
  - at configurable places at move (number, colour)
  + conclusion: not a good idea and should not be part of python chess, also python chess only export into svg, could be a good feature for the python CLI tool or for md2mm, should explore if svgs are better (python chess can render arrows and maybe NAGs on the board soon as well)
- use edn_format lib to print edn [low prio]
- implement the commandline interface for game reading/exporting into json/edn
