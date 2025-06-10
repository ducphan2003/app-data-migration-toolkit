from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union


class SuggestVocabQuery(BaseModel):
    input: str      = Field(..., description="The input text to process")
    question: str   = Field(..., description="The question related to the input text")


class CorrectWritingBody(BaseModel):
    input: Union[str, Dict, List]   = Field(None, description="The input text to process")
    type: str                       = Field(None, description="The question related to the input text")
    answer_id: Optional[int]        = Field(None, description="The question related to the input text")
    question: Optional[str]         = Field(None, description="The question related to the input text")
    image: Optional[str]            = Field(None, description="The image related to the input text")
    link_image: Optional[str]       = Field(None, description="The link of the image")
    description: Optional[str]      = Field(None, description="The description of the image")
    media_type: Optional[str]       = Field(None, description="The type of the image")
    skill: Optional[str]            = Field('WRITING', description="The type of the skill")

class SuggestVocabExample(BaseModel):
    example_id: str
    example_text: str


class ActivateVersionBody(BaseModel):
    key: str
    version: int


class SuggestVocab(BaseModel):
    translation: str
    synonyms: Dict[str, str]
    examples: List[SuggestVocabExample]


class LRGRCommentsTask1(BaseModel):
    id: str
    comment: str
    class_name: Optional[str]   = Field(None, alias="class")


class LRGRCorrectionTask1(BaseModel):
    data: str
    comments: List[LRGRCommentsTask1]
    clean_data: str


class LRGRCommentsTask2(BaseModel):
    id: str
    comment: str
    error_id: Optional[int]   = Field(None, alias="error_id")
    class_name: Optional[str]   = Field(None, alias="class_name")


class LRGRCorrectionTask2(BaseModel):
    data: str
    comments: List[LRGRCommentsTask2]
    clean_data: str


class RemoteConfigRequest(BaseModel):
    key: str    = Field(..., description="The configuration key")
    value: str  = Field(..., description="The configuration value")


class ExtraTRCCComment(BaseModel):
    error_type: str     = Field("task_response")
    is_important: bool  = Field(False)

    def to_dict(self):
        return self.dict()


class TRCCComments(BaseModel):
    id: str
    comment: str
    suggestion: str
    extra: Optional[ExtraTRCCComment] = ExtraTRCCComment()


class TRCCCorrection(BaseModel):
    data: str
    comments: List[TRCCComments]


class VerifyWritingBody(BaseModel):
    input: str      = Field(..., description="The input text to process")
    answer_id: int  = Field(..., description="The question related to the input text")


class CompletionInput(BaseModel):
    provider: str                                       = Field("")
    model: str                                          = Field(...)
    extra_models: Optional[List[str]]                   = Field([])
    prompt_task: Optional[str]                          = Field(None)
    prompt: str                                         = Field(None)
    documentation: str                                  = Field(None)
    system: Optional[str]                               = Field("")
    link_image: Optional[str]                           = Field("")
    media_type: Optional[str]                           = Field("")
    vision_type: Optional[str]                          = Field("")
    prefill: Optional[str]                              = Field("")
    action: Optional[str]                               = Field("")
    ref: Optional[str]                                  = Field("")
    ref_id: Optional[str]                               = Field("")
    history: Optional[List[str]]                        = Field([])
    additional_media: Optional[List[Dict[str, str]]]    = Field([])
    max_tokens: Optional[int]                           = Field(None, description="Maximum number of tokens to generate")
    max_reasoning_tokens: Optional[int]                 = Field(None, description="Maximum number of tokens for reasoning")
    effort_reasoning: Optional[str]                     = Field(None, description="Effort level for reasoning, e.g., 'low', 'medium', 'high'")
    temperature: Optional[float]                        = Field(None, description="Temperature for the model response, controls randomness")
    top_p: Optional[float]                              = Field(None, description="Top-p sampling parameter for the model response")


class CompletionConfig(BaseModel):
    provider: str                                       = Field("")
    model: str                                          = Field("")
    extra_models: Optional[List[str]]                   = Field([])
    thinking: bool                                      = Field(None)
    vision: bool                                        = Field(None)
    action: str                                         = Field("")
    intro_prompt: str                                   = Field("")
    documentation: str                                  = Field(None)
    link_image: str                                     = Field("")
    media_type: str                                     = Field("")
    vision_type: str                                    = Field("")
    additional_media: Optional[List[Dict[str, str]]]    = Field([])
    max_tokens: Optional[int]                           = Field(None, description="Maximum number of tokens to generate")
    max_reasoning_tokens: Optional[int]                 = Field(None, description="Maximum number of tokens for reasoning")
    effort_reasoning: Optional[str]                     = Field(None, description="Effort level for reasoning, e.g., 'low', 'medium', 'high'")
    temperature: Optional[float]                        = Field(None, description="Temperature for the model response, controls randomness")
    top_p: Optional[float]                              = Field(None, description="Top-p sampling parameter for the model response")


class WritingScoreDetailTask2(BaseModel):
    TR: Optional[int] = Field(None)
    CC: Optional[int] = Field(None)
    LR: Optional[int] = Field(None)
    GR: Optional[int] = Field(None)


class WritingScoreDetailTask1(BaseModel):
    TA: Optional[int] = Field(None)
    CC: Optional[int] = Field(None)
    LR: Optional[int] = Field(None)
    GR: Optional[int] = Field(None)


class BandScoreTask2(BaseModel):
    band_score: float
    band_score_detail: WritingScoreDetailTask2


class BandScoreTask1(BaseModel):
    band_score: float
    band_score_detail: WritingScoreDetailTask1

class UpgradeSpeakingPart1Correction(BaseModel):
    data: str
    raw_text: str

class LRGRCommentsTask1Ver2(BaseModel):
    id: str
    comment: str
    error_id: Optional[int]   = Field(None, alias="error_id")
    class_name: Optional[str]   = Field(None, alias="class_name")


class LRGRCorrectionTask1Ver2(BaseModel):
    data: str
    comments: List[LRGRCommentsTask1Ver2]
    clean_data: str
    
class SpeakingLRGRBandScore(BaseModel):
    LR: Optional[int] = Field(None)
    GRA: Optional[int] = Field(None)
    
class SpeakingFLBRBandScore(BaseModel):
    FC: Optional[int] = Field(None)
    PR: Optional[int] = Field(None)
    
class CorrectSpeakingBody(BaseModel):
    transcript: Union[str, Dict, List]  = Field(None, description="The transcript text to process")
    type: str                           = Field(None, description="The type of the question related to the transcript")
    answer_id: int                      = Field(None, description="The answer ID related to the transcript")
    duration: Optional[float]           = Field(None, description="The duration of the speaking task in seconds")
    number_of_words: Optional[int]      = Field(None, description="The number of words in the transcript")
    speed: Optional[str]                = Field(None, description="The speaking speed")
    overall_confidence: Optional[str]   = Field(None, description="The overall confidence score of the speaking task")
    confidence_range: Optional[str]     = Field(None, description="The confidence range of the speaking task")
    utterances: Optional[str]           = Field(None, description="The utterances in the speaking task")
    