# Cursor IDE rules

This folder contains a set of Cursor IDE rules that can be used in your projects.

These rules have been collected with the following goals in mind:
* They are not part of the LLM Training
* They are actionable
* They are explicit

## How to use the rules

Copy the entire .cursor folder to the root of your project and restart the Cursor IDE.

The rules directly defined in the .cursor folder will then be applied depending on the language you are working on.
These rules are not specific to any framework or tool, so they can be used in any project.

There are also some rules defined in the 'extra' folder. Based on the framework and tools you are using, you can move them in your '.cursor/rule' folder to have them applied.
After moving a rule file, restart the Cursor IDE to apply the changes.

## Contributing

If some corrective instructions need to be often added after AI code generation, it could be worth adding them as a rule here.
When adding a new rule, please make sure to:
* Put the rule in the correct file (Is the rule specific to a language? A framework? A tool?)
* It is not part of the LLM training
* It is actionable and explicit

Remember that any rule defined will use tokens in the AI context, leaving fewer tokens for the other tasks AI has to perform.

