from ..math.math_handler import MathTaskHandler
from typing import Dict
from skythought_evals.util.model_utils import MODEL_TO_NAME


class AMC23TaskHandler(MathTaskHandler):
    def generate_prompt(self, problem: Dict, model):
        if "DeepSeek-R1" in MODEL_TO_NAME[model]:
            return self.task_config.templating_parameters["r1_template"].format(
                prompt=problem["problem"]
            )
        else:
            return self.task_config.templating_parameters["regular_template"].format(
                prompt=problem["problem"]
            )

    def make_conversations(self, data, system_prompt, model=None):
        conversations = []
        for problem in data:
            prompt_text = self.generate_prompt(problem, model)
            conversations.append(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_text},
                ]
            )
        return conversations

    def load_and_filter_dataset(
        self, start, end, split=None, subset=None, difficulty=None, args=None
    ):
        train_data = self.load_dataset(subset=subset, split=split).to_pandas()
        filtered_data = train_data[train_data["url"].str.contains("2023", na=False)]
        return filtered_data.iloc[start:end] if end > 0 else filtered_data.iloc[start:]
