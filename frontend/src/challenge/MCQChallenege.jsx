import "react"
import { useState } from "react"

export function MCQChallenge({ challenge, showExplanation = false, onCorrect }) {
  const [selectedOption, setSelectedOption] = useState(null)
  const [shouldShowExplanation, setShouldShowExplanation] = useState(showExplanation)
  const [rating, setRating] = useState(null)

  const options =
    typeof challenge.options === "string"
      ? JSON.parse(challenge.options)
      : challenge.options

  const handleOptionSelect = (index) => {
    if (selectedOption !== null) {
      return
    }
    setSelectedOption(index)
    setShouldShowExplanation(true)
    if (index === challenge.correct_answer_id && onCorrect) {
      onCorrect()
    }
  }

  const getOptionClass = (index) => {
    if (selectedOption === null) {
      return "option"
    }
    if (index === challenge.correct_answer_id) {
      return "option correct"
    }
    if (index === selectedOption && index !== challenge.correct_answer_id) {
      return "option incorrect"
    }
    return "option"
  }

  return (
    <div className="challenge-card">
      <span className={`difficulty-badge ${challenge.difficulty}`}>
        {challenge.difficulty.charAt(0).toUpperCase() + challenge.difficulty.slice(1)}
      </span>
      <h3 className="challenge-title">{challenge.title}</h3>
      <div className="options">
        {options.map((option, index) => (
          <div
            className={getOptionClass(index)}
            key={index}
            onClick={() => handleOptionSelect(index)}
            tabIndex={0}
            role="button"
            aria-pressed={selectedOption === index}
            style={{ outline: "none" }}
          >
            {option}
          </div>
        ))}
      </div>
      {shouldShowExplanation && selectedOption !== null && (
        <div className="explanation">
          <h4>Explanation</h4>
          <p>{challenge.explanation}</p>
        </div>
      )}
      <div className="rating">
        <span>Rate this challenge:</span>
        <button
          aria-label="Thumbs up"
          onClick={() => setRating("up")}
          style={{ color: rating === "up" ? "#43a047" : undefined }}
        >👍</button>
        <button
          aria-label="Thumbs down"
          onClick={() => setRating("down")}
          style={{ color: rating === "down" ? "#e53935" : undefined }}
        >👎</button>
      </div>
    </div>
  )
}