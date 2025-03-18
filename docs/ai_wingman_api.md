# AI Wingman API

The AI Wingman API provides endpoints for processing conflict resolution sessions. It analyzes transcripts of conversations, identifies conflict patterns, and generates structured dialogues.

## Endpoints

### POST /api/v1/ai-wingman/conversation

Process a conflict resolution conversation.

#### Request

```json
{
  "transcript": "String containing the transcript of the conversation",
  "conflict_types": ["List of conflict types"],
  "partner_a_background": "String containing background information about partner A",
  "partner_b_background": "String containing background information about partner B"
}
```

#### Response

```json
{
  "conflict_analysis": "String containing analysis of the conflict",
  "dialogue_script": "String containing dialogue for the participants to read aloud",
  "empathy_guidance": "String containing guidance for building empathy",
  "resolution_strategies": "String containing strategies for resolving the conflict"
}
```

#### Example

**Request:**

```json
{
  "transcript": "Partner A: You never help with the housework! I'm always the one cleaning up after everyone.\nPartner B: That's not true! I do plenty around here. You just don't notice it.",
  "conflict_types": ["Household responsibilities", "Communication breakdown"],
  "partner_a_background": "Partner A grew up in a very organized household where chores were strictly divided.",
  "partner_b_background": "Partner B grew up in a more relaxed household where chores were done as needed."
}
```

**Response:**

```json
{
  "conflict_analysis": "This conflict centers around household responsibilities and different perceptions of contribution...",
  "dialogue_script": "Partner A: I feel overwhelmed when I perceive that I'm doing most of the housework...\nPartner B: I understand that you feel overwhelmed, and I want to help...",
  "empathy_guidance": "For Partner A: Consider that Partner B may have a different threshold for noticing when things need to be cleaned...\nFor Partner B: Recognize that Partner A feels overwhelmed and may need more visible support...",
  "resolution_strategies": "Short-term: Create a clear chore division that respects both partners' preferences...\nLong-term: Schedule regular check-ins to discuss how the household management is working..."
}
```

## Error Responses

### 500 Internal Server Error

If there's an error processing the request, the API will return a 500 status code with an error message:

```json
{
  "detail": "Error message"
}
```
