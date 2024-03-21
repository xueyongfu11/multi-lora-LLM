import os
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from config import common_config


class MultiLora:
    def __init__(self, args):
        self.args = args
        self.device = torch.device(f'cuda')
        self.model_name = self.args.base_model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        self.tokenizer.padding_side = 'left'
        self.lora2path = common_config.lora2path

        inference_config = {}
        if args.use_qlora:
            from transformers import BitsAndBytesConfig
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            inference_config['quantization_config'] = bnb_config
            inference_config['device_map'] = 'auto'

        if args.pipline:
            max_memory = {i: '24000MB' for i in range(torch.cuda.device_count())}
            inference_config['max_memory'] = max_memory
            inference_config['device_map'] = 'auto'

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            # load_in_4bit=True,  # transformers==4.38注释该参数
            **inference_config,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        ).eval()
        if not args.use_qlora and not args.pipline:
            self.model.to(self.device)
        generation_config = GenerationConfig.from_pretrained(self.model_name, trust_remote_code=True)
        generation_config.update( max_new_tokens=args.max_new_tokens, temperature=0.001)
        print(generation_config)
        self.model.generation_config = generation_config

        if args.origin_llm:
            return
        assert not (args.load_just_one_lora and args.load_all_lora)
        if args.load_just_one_lora:
            self.load_lora()
        else:
            self.load_all_loras()
            self.cur_lora = None

    def load_lora(self):
        self.model = PeftModel.from_pretrained(self.model, self.args.lora_path)

    def load_all_loras(self):
        for i, (adapter_name, path) in enumerate(common_config.lora2path):
            if i == 0:
                self.model = PeftModel.from_pretrained(self.model, path, adapter_name=adapter_name)
                continue
            self.model.load_adapter(path, adapter_name=adapter_name)

    def set_lora(self, name):
        self.cur_lora = name
        self.model.set_adapter(name)

    def get_cur_lora(self):
        return self.cur_lora

    def gene_response(self, text, non_lora=False):
        if 'Qwen1.5' in self.model_name:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ]
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
            if non_lora:
                with self.model.disable_adapter():
                    generated_ids = self.model.generate(inputs=model_inputs.input_ids)
            else:
                generated_ids = self.model.generate(inputs=model_inputs.input_ids)
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        else:
            # qwen1.0
            if non_lora:
                with self.model.disable_adapter():
                    response, _ = self.model.chat(self.tokenizer, text, history=None)
            else:
                response, _ = self.model.chat(self.tokenizer, text, history=None)
        return response

    def gene_batch_response(self, contents, non_lora=False):
        # 仅支持qwen1.5
        inputs = []
        for line in contents:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": line}
            ]
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            inputs.append(text)
        model_inputs = self.tokenizer(inputs, padding="longest", return_tensors='pt').to(self.device)

        if non_lora:
            with self.model.disable_adapter():
                # attention_mask必须传入，默认attention_mask的计算方式不正确
                generated_ids = self.model.generate(
                    inputs=model_inputs.input_ids,
                    attention_mask=model_inputs.attention_mask
                )
        else:
            generated_ids = self.model.generate(
                inputs=model_inputs.input_ids,
                attention_mask=model_inputs.attention_mask
            )

        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        return response

    def predict(self, contents):
        # 仅支持qwen1.5
        inputs = []
        for line in contents:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": line}
            ]
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            inputs.append(text)
        model_inputs = self.tokenizer(inputs, padding="longest", return_tensors='pt').to(self.device)

        generated_ids = self.model.generate(
            inputs=model_inputs.input_ids,
            attention_mask=model_inputs.attention_mask
        )

        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        return response
