from pydantic import BaseModel, model_validator


class Highscore(BaseModel):
    name: str
    score: int

    @model_validator(mode="after")
    def validate_values(self) -> "Highscore":
        if not self.name:
            raise ValueError("Highscore name can not be empty")
        if not self.score:
            raise ValueError("Highscore score can not be empty")
        return self
