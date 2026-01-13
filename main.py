# from agenticAiLab.callingGenAiApis.day2_LlmAsAJudgeWithoutTools import chat
import gradio as gr
from agenticAiLab.callingGenAiApis.day3_LlmAsAJudgeWithTools import aboutUser

# from agenticAiLab.callingGenAiApis.day3_LlmAsAJudgeWithTools import Me

# me = Me()
# # push("This is a test push notification from the main.py file.")
# gr.ChatInterface(
#     fn=me.callGradle,
# ).launch()

if __name__ == "__main__":
    text = aboutUser()
    print(text)
