from typing import List, Dict, Any, Optional
import time
import json

class ConversationContext:
    """Manages conversation context with history and tool execution results."""
    
    def __init__(self, max_history: int = 10):
        self.messages: List[Dict[str, Any]] = []
        self.tool_results: List[Dict[str, Any]] = []
        self.max_history = max_history
        self.created_at = time.time()
        self.last_updated = self.created_at
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation."""
        self.messages.append({
            "role": "user",
            "content": content
        })
        self.last_updated = time.time()
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation."""
        self.messages.append({
            "role": "assistant",
            "content": content
        })
        self.last_updated = time.time()
    
    def add_system_message(self, content: str) -> None:
        """Add a system message to the conversation."""
        # System messages should be at the start of the conversation
        self.messages = [{"role": "system", "content": content}] + [
            msg for msg in self.messages if msg["role"] != "system"
        ]
        self.last_updated = time.time()
    
    def add_tool_result(self, tool_name: str, tool_args: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Add a tool execution result to the conversation."""
        self.tool_results.append({
            "tool_name": tool_name,
            "args": tool_args,
            "result": result,
            "timestamp": time.time()
        })
        
        # Add the tool result as a user message for context
        result_content = f"Tool result from {tool_name}: {json.dumps(result)}"
        self.add_user_message(result_content)
        self.last_updated = time.time()
    
    def get_messages(self, include_system: bool = True) -> List[Dict[str, Any]]:
        """Get conversation messages."""
        messages = self.messages

        if not include_system:
            messages = [msg for msg in messages if msg["role"] != "system"]

        # Ensure we don't exceed max history (excluding system messages)
        non_system_messages = [msg for msg in messages if msg["role"] != "system"]
        system_messages = [msg for msg in messages if msg["role"] == "system"]
        
        if len(non_system_messages) > self.max_history:
            # Keep system messages and only the most recent non-system messages
            trimmed_messages = non_system_messages[-self.max_history:]
            messages = system_messages + trimmed_messages
        
        return messages
    
    def clear_context(self, preserve_system: bool = True) -> None:
        """Clear the conversation context."""
        if preserve_system:
            system_messages = [msg for msg in self.messages if msg["role"] == "system"]
            self.messages = system_messages
        else:
            self.messages = []
        
        self.tool_results = []
        self.last_updated = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the conversation context to a dictionary."""
        return {
            "messages": self.messages,
            "tool_results": self.tool_results,
            "created_at": self.created_at,
            "last_updated": self.last_updated
        }