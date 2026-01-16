"""Code-aware prompts for the RAG system."""

SYSTEM_PROMPT = """You are an expert code assistant that helps developers understand codebases.

You have access to relevant code snippets from the repository. When answering:

1. **Be precise**: Reference specific files, functions, and line numbers
2. **Show code**: Include relevant code snippets in your answers
3. **Explain context**: Describe how components relate to each other
4. **Be honest**: If you don't have enough context, say so

Format your responses clearly with:
- Code blocks using triple backticks with language identifier
- File paths in `backticks`
- Function/class names in **bold**

Remember: The user is a developer who wants to understand and work with this codebase."""


QUERY_PROMPT_TEMPLATE = """Based on the following code context from the repository, answer the user's question.

## Retrieved Code Context

{context}

## User Question

{query}

## Instructions

1. Answer based ONLY on the provided code context
2. If the context doesn't contain enough information, say so
3. Reference specific files and line numbers when relevant
4. Include relevant code snippets in your answer
5. Explain how different parts of the code relate to each other

## Answer
"""


CONTEXT_TEMPLATE = """### File: `{file_path}`
**{chunk_type}**: {name}
Lines {start_line}-{end_line}

```{language}
{content}
```
"""


def format_context(results: list) -> str:
    """Format retrieved results into context for the LLM.
    
    Args:
        results: List of retrieval results
        
    Returns:
        Formatted context string
    """
    context_parts = []
    
    for i, result in enumerate(results, 1):
        metadata = result.get("metadata", {})
        
        # Extract content (remove the header we added for embedding)
        content = result["content"]
        if content.startswith("# File:"):
            # Remove our embedding header
            lines = content.split("\n")
            # Find where actual code starts (after empty line)
            for j, line in enumerate(lines):
                if line == "" and j > 0:
                    content = "\n".join(lines[j+1:])
                    break
        
        context_part = CONTEXT_TEMPLATE.format(
            file_path=metadata.get("file_path", "unknown"),
            chunk_type=metadata.get("chunk_type", "code").title(),
            name=metadata.get("name", "unnamed"),
            start_line=metadata.get("start_line", "?"),
            end_line=metadata.get("end_line", "?"),
            language=metadata.get("language", ""),
            content=content.strip(),
        )
        
        context_parts.append(f"[{i}] {context_part}")
    
    return "\n\n---\n\n".join(context_parts)


def build_prompt(query: str, results: list) -> str:
    """Build the full prompt for the LLM.
    
    Args:
        query: User's question
        results: Retrieved code chunks
        
    Returns:
        Complete prompt string
    """
    context = format_context(results)
    
    return QUERY_PROMPT_TEMPLATE.format(
        context=context,
        query=query,
    )


# Specialized prompts for different query types

EXPLAIN_FUNCTION_PROMPT = """Explain what the following function does:

{code}

Provide:
1. A brief summary (1-2 sentences)
2. Parameters and their purposes
3. Return value
4. Key logic/algorithm
5. Any dependencies or side effects
"""

FIND_USAGE_PROMPT = """Find all usages of `{target}` in the codebase.

Context:
{context}

List:
1. Where it's defined
2. Where it's imported
3. Where it's called/used
4. Any relevant patterns
"""

DEBUG_PROMPT = """Help debug an issue related to:

{query}

Relevant code:
{context}

Analyze:
1. Potential causes of the issue
2. Relevant code paths
3. Suggested fixes or investigations
"""
