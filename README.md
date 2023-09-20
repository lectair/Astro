# Astro

An easy way to interact with GPT in your scripts obtaining reliable outputs.
You can easily pass arguments and motivations to GPT and it will do what your software needs.

Work in progress.

Sample Code:
```
app = Astro()
app.setAPIKey("sk-0WkQOuFYROXXXXXXXXXXXXXXXXXXXXXfUiAKxsruO6HyjLoG")
app.setVocation("You are an open world video game script that takes some parameters and calculates the response based on those parameters. The parameters that you get are details of your environment. The response that you must return is the reaction you think you should take based on the parameters. Take into account that you should have a random personality. You MUST ALWAYS respond in the format in which you are provided with the following example.")
app.setValidValues(["run", "attack", "curse", "cower", "give_item"])
app.setExamples("USER: {EntityType: 'Pedestrian', EntityHealth: '45%', NearEntities: [{ {EntityType: 'Cat', LastTimeSeenSecondsAgo: 42, EntityHealth: '100%', EntityDistanceMeters: 45, IsHostile: False}, {EntityType: 'Pedestrian', LastTimeSeenSecondsAgo: 6, EntityHealth: '0%', EntityDistanceMeters: 34, IsHostile: False}}, {EntityType: 'Character', LastTimeSeenSecondsAgo: 0, EntityHealth: '86%', EntityDistanceMeters: 2, IsHostile: True}], EntityWeapons: []}  {ResponseMessage: 'Don't punch me motherfucker! Im outta this' ResponseAction: 'run'}")
app.newInstruction("GTA-V")
app.addInstructionData("GTA-V", "EntityType", "Pedestrian")
app.addInstructionData("GTA-V", "EntityHealth", "25%")
print(app.getInstructions())
print(app.sendLLMRequest())

```
Sample Response:
```
{
  "id": "chatcmpl-80ktjHJmZeFvmoSC4hQtDpIztHm1D",
  "object": "chat.completion",
  "created": 1695190967,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "ResponseMessage: \"Oh no, I better be careful! I need to find a safe place to hide!\"\nResponseAction: \"cower\""
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 349,
    "completion_tokens": 29,
    "total_tokens": 378
  }
}
```
