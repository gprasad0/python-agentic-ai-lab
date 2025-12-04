from agenticAiLab.callingGenAiApis.day2_LlmAsAJudgeWithoutTools import chat
import gradio as gr


gr.ChatInterface(
    fn=chat,
).launch()
