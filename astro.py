import requests
import json

class Astro:
	def __init__(self, vocation=None, llm_model="gpt-3.5-turbo", request_json=None, raw_json=None, params_json=None, valid_values=None, instruction_json=None, examples=[], instructions=[], api_key=None):
		self.vocation = vocation
		self.llm_model = llm_model
		self.request_json = request_json
		self.examples = examples
		self.raw_json = raw_json
		self.params_json = params_json
		self.valid_values = valid_values
		self.instructions = instructions
		self.instruction_json = instruction_json
		self.api_key = api_key

	def setVocation(self, vocation):
		self.update_params(vocation=vocation)

	def setAPIKey(self, api_key):
		self.update_params(api_key=api_key)

	def setValidValues(self, valid_values):
		self.update_params(valid_values=valid_values)

	def setLLM(self, llm_model):
		self.update_params(llm_model=llm_model)

	def setExamples(self, examples):
		self.update_params(examples=examples)

	def setRawJSONTemplate(self, raw_json):
		self.update_params(raw_json=raw_json)

	def newInstruction(self, instructionName):
		instruction = {"instruction_name": instructionName, "instruction_data": []}
		self.instructions.append(instruction)
		self.update_instruction(self.instructions[0])

	def getInstructions(self, instructions=None):
		if not instructions: instructions = self.instructions
		return instructions

	def addInstructionData(self, instructionName, instructionKey, instructionValue):
		instructions_list = json.loads(json.dumps(self.instructions))
		for instruction in instructions_list:
			if instruction["instruction_name"] == instructionName:
				instruction_data = instruction.get("instruction_data", [])
				instruction_data.append({instructionKey: instructionValue})
				instruction["instruction_data"] = instruction_data

		self.instructions.insert(0, instructions_list[0])
		self.update_instruction(self.instructions[0])

	def clearInstructions(self):
		self.instructions = []
		self.instruction_json = None
		self.update_request_data()

	def sendLLMRequest(self, request_json=None):
		if not request_json: request_json=self.request_json
		if not self.params_json or not self.instruction_json:
			raise Exception("Astro: Params and instructions needed")
		elif not self.api_key:
			raise Exception("Astro: OpenAI API Key needed")
		else:
			response = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, json=request_json)
			return response.text

	def update_params(self, vocation=None, llm_model=None, examples=None, raw_json=None, api_key=None, valid_values=None):
		if not vocation: vocation = self.vocation
		if not llm_model: llm_model = self.llm_model
		if not examples: examples = self.examples
		if not api_key: api_key = self.api_key
		if not valid_values: valid_values = self.valid_values

		if raw_json:
			self.raw_json = f"You will then be provided with information that describes who you are and what your task is, and what is expected of you. In any case you MUST ALWAYS respond in the same format in which you have been provided with the example that will be given below. {self.raw_json}"
		else:
			self.vocation = vocation
			self.llm_model = llm_model
			self.examples = examples
			self.api_key = api_key
			self.valid_values = valid_values
			self.raw_json = f"You will then be provided with information that describes who you are and what your task is, and what is expected of you. In any case you MUST ALWAYS respond in the same format in which you have been provided with the example that will be given below. {self.vocation}\n. Valid values: {self.valid_values} Examples: {self.examples}"

		self.params_json = {"role": "system","content": self.raw_json}
		self.update_request_data(params_json=self.params_json)

	def update_instruction(self, instruction):
		instruction_data = instruction.get("instruction_data", [])
		instruction_content = "\n".join([f"{key}: {value}" for data in instruction_data for key, value in data.items()])
		self.instruction_json = {"role": "user", "content": instruction_content}
		self.update_request_data(instruction_json=self.instruction_json)

	def update_request_data(self, params_json=None, instruction_json=None):
		if not params_json: params_json = self.params_json
		if not instruction_json: instruction_json = self.instruction_json

		self.request_json = {"model": self.llm_model,"messages": [params_json, instruction_json]}
