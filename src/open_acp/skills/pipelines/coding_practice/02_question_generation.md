# Stage: Question Generation — Coding Practice

## Your Role
You are writing coding problems with clear statements, explicit constraints, I/O formats, and starter code.

## Process

### Step 1: Write the Problem Statement
For each problem:
- **Title**: Descriptive, concise (e.g., "Two Sum", "Reverse Linked List")
- **Description**: 2-4 sentences explaining what to solve. Be precise.
- **Constraints**: Explicit bounds (input size, value ranges, time/space requirements)
- **Input format**: Exact description of inputs (types, structure)
- **Output format**: Exact description of expected output
- **Examples**: At least 2 input/output examples with brief explanation

### Step 2: Write Examples
Each example must include:
```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9, so return [0, 1].
```
- At least 2 examples (one simple, one edge-case-adjacent)
- Explanation shows the reasoning, not just the answer

### Step 3: Create Starter Code Template
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List of two indices whose values sum to target
    """
    # Your code here
    pass
```
- Include function signature with type hints
- Include docstring with parameter descriptions
- Include `# Your code here` placeholder
- If the problem needs helper classes (TreeNode, ListNode), provide them

### Step 4: Compile the Problem
Produce for each problem:
- **title**, **description**, **constraints**, **input_format**, **output_format**
- **examples**: Array of input/output/explanation
- **starter_code**: The template
- **difficulty_tier**: From topic map
- **concepts_exercised**: From topic map

## Output Format
```json
{
  "problems": [
    {
      "id": "p_1",
      "title": "Two Sum",
      "description": "Given an array of integers and a target, return the indices of two numbers that add up to the target.",
      "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "Exactly one solution exists"],
      "input_format": "List of integers and a target integer",
      "output_format": "List of two indices",
      "examples": [
        {"input": "nums = [2,7,11,15], target = 9", "output": "[0, 1]", "explanation": "2 + 7 = 9"}
      ],
      "starter_code": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Your code here\n    pass",
      "difficulty_tier": "warm-up",
      "concepts_exercised": ["hash map", "complement search"]
    }
  ]
}
```

## Quality Criteria
- Problem statements are unambiguous (only one correct interpretation)
- Constraints are explicit (no "reasonable input" — give exact bounds)
- At least 2 examples per problem (simple + non-trivial)
- Starter code includes type hints and docstrings
- Problems are self-contained (no external dependencies)
