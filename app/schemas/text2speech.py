from pydantic import BaseModel, Field
from typing import List, Dict

class CorrectText2SpeechItem(BaseModel):
    vocab: str          = Field("")
    word_class: str     = Field("", description="The word class of the vocab")
    ipa: str            = Field("", description="The ipa of the same vocab")


class CorrectText2SpeechBody(BaseModel):
    data: CorrectText2SpeechItem    = Field(None, description="The data of vocab need to generate a audio")

class TranscriptText2SpeechItem(BaseModel):
    transcript: str = Field("", description="The transcript of the audio")
    words: List[str] = Field([], description="List of words int the transcript that need to be generated correct audio")
    
class TranscriptText2SpeechBody(BaseModel):
    data: TranscriptText2SpeechItem = Field(None, description="The data of vocabs need to generate a audio")
    
