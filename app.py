#!/usr/bin/env python3
"""
Multi-Agent Task 3 - Advanced AI Agent Framework
Implements a sophisticated multi-agent system with inter-agent communication,
task delegation, and collaborative problem-solving capabilities.
"""

import asyncio
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Enumeration of agent types"""
    RESEARCHER = "researcher"
    ANALYZER = "analyzer"
    PLANNER = "planner"
    EXECUTOR = "executor"


class MessageType(Enum):
    """Message types for inter-agent communication"""
    QUERY = "query"
    RESPONSE = "response"
    DELEGATION = "delegation"
    FEEDBACK = "feedback"
    STATUS = "status"


@dataclass
class Message:
    """Message structure for agent communication"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: MessageType = MessageType.QUERY
    sender_id: str = ""
    receiver_id: str = ""
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: int = 1

    def to_dict(self) -> Dict:
        """Convert message to dictionary"""
        return {
            'message_id': self.message_id,
            'message_type': self.message_type.value,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'timestamp': self.timestamp,
            'priority': self.priority
        }


@dataclass
class Task:
    """Task structure for agent execution"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    action: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    result: Optional[Dict] = None


class BaseAgent(ABC):
    """Base class for all agent types"""

    def __init__(self, agent_id: str, agent_type: AgentType):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_queue: List[Message] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.task_history: List[Task] = []
        self.is_active = True
        logger.info(f"Agent {self.agent_id} initialized as {agent_type.value}")

    def receive_message(self, message: Message) -> None:
        """Receive a message from another agent"""
        if message.receiver_id == self.agent_id:
            self.message_queue.append(message)
            logger.info(f"Agent {self.agent_id} received message {message.message_id}")

    async def process_message(self, message: Message) -> Message:
        """Process incoming message and generate response"""
        logger.info(f"Processing message {message.message_id}")
        response = Message(
            message_type=MessageType.RESPONSE,
            sender_id=self.agent_id,
            receiver_id=message.sender_id,
            content={'status': 'processed'}
        )
        return response

    async def execute_task(self, task: Task) -> Dict:
        """Execute assigned task"""
        task.status = "running"
        logger.info(f"Agent {self.agent_id} executing task {task.task_id}")
        try:
            result = await self._perform_action(task.action, task.parameters)
            task.status = "completed"
            task.result = result
            self.task_history.append(task)
            return {'status': 'success', 'result': result}
        except Exception as e:
            task.status = "failed"
            logger.error(f"Task execution failed: {str(e)}")
            return {'status': 'failed', 'error': str(e)}

    @abstractmethod
    async def _perform_action(self, action: str, parameters: Dict) -> Dict:
        """Perform specific action (implemented by subclasses)"""
        pass

    def get_status(self) -> Dict:
        """Get agent status"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type.value,
            'is_active': self.is_active,
            'message_queue_size': len(self.message_queue),
            'task_history_count': len(self.task_history),
            'knowledge_base_size': len(self.knowledge_base)
        }

    def shutdown(self) -> None:
        """Shutdown agent gracefully"""
        self.is_active = False
        logger.info(f"Agent {self.agent_id} shutdown")


class ResearchAgent(BaseAgent):
    """Agent specialized in research and data gathering"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.RESEARCHER)
        self.data_sources = []

    async def _perform_action(self, action: str, parameters: Dict) -> Dict:
        """Perform research action"""
        if action == "gather_data":
            topic = parameters.get('topic', '')
            logger.info(f"Gathering data on: {topic}")
            return {
                'action': 'gather_data',
                'topic': topic,
                'data': f"Research data for {topic}",
                'sources': 5
            }
        return {'action': action, 'status': 'unknown_action'}


class AnalysisAgent(BaseAgent):
    """Agent specialized in data analysis"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.ANALYZER)

    async def _perform_action(self, action: str, parameters: Dict) -> Dict:
        """Perform analysis action"""
        if action == "analyze_data":
            data = parameters.get('data', {})
            depth = parameters.get('depth', 'basic')
            logger.info(f"Analyzing data with depth: {depth}")
            return {
                'action': 'analyze_data',
                'insights': f"Key insights from {depth} analysis",
                'patterns': 3,
                'confidence_score': 0.85
            }
        return {'action': action, 'status': 'unknown_action'}


class PlanningAgent(BaseAgent):
    """Agent specialized in planning and strategy"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.PLANNER)

    async def _perform_action(self, action: str, parameters: Dict) -> Dict:
        """Perform planning action"""
        if action == "create_strategy":
            timeline = parameters.get('timeline', '1_month')
            logger.info(f"Creating strategy for: {timeline}")
            return {
                'action': 'create_strategy',
                'timeline': timeline,
                'phases': 3,
                'milestones': 5,
                'resource_requirements': 'moderate'
            }
        return {'action': action, 'status': 'unknown_action'}


class ExecutionAgent(BaseAgent):
    """Agent specialized in task execution"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.EXECUTOR)
        self.execution_count = 0

    async def _perform_action(self, action: str, parameters: Dict) -> Dict:
        """Perform execution action"""
        if action == "implement_plan":
            resources = parameters.get('resources', 'basic')
            self.execution_count += 1
            logger.info(f"Implementing plan with resources: {resources}")
            return {
                'action': 'implement_plan',
                'resources': resources,
                'execution_count': self.execution_count,
                'completion_percentage': 100,
                'status': 'completed'
            }
        return {'action': action, 'status': 'unknown_action'}


class AgentRegistry:
    """Central registry for agent management"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[Message] = []
        self.task_queue: List[Task] = []
        logger.info("Agent Registry initialized")

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent in the registry"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent {agent.agent_id} registered")

    def create_agent(self, agent_type: str) -> BaseAgent:
        """Create and register a new agent"""
        agent_id = f"{agent_type}_{str(uuid.uuid4())[:8]}"
        
        if agent_type == "researcher":
            agent = ResearchAgent(agent_id)
        elif agent_type == "analyzer":
            agent = AnalysisAgent(agent_id)
        elif agent_type == "planner":
            agent = PlanningAgent(agent_id)
        elif agent_type == "executor":
            agent = ExecutionAgent(agent_id)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        self.register_agent(agent)
        return agent

    def send_message(self, message: Message) -> bool:
        """Send message from one agent to another"""
        if message.receiver_id not in self.agents:
            logger.warning(f"Receiver {message.receiver_id} not found")
            return False
        
        receiver = self.agents[message.receiver_id]
        receiver.receive_message(message)
        logger.info(f"Message sent from {message.sender_id} to {message.receiver_id}")
        return True

    async def execute_task(self, task: Task) -> Dict:
        """Execute task on designated agent"""
        if task.agent_id not in self.agents:
            logger.error(f"Agent {task.agent_id} not found")
            return {'status': 'failed', 'error': 'Agent not found'}
        
        agent = self.agents[task.agent_id]
        result = await agent.execute_task(task)
        self.task_queue.append(task)
        return result

    def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get status of specific agent"""
        if agent_id not in self.agents:
            return None
        return self.agents[agent_id].get_status()

    def get_all_agents_status(self) -> Dict[str, Dict]:
        """Get status of all agents"""
        return {agent_id: agent.get_status() 
                for agent_id, agent in self.agents.items()}

    def shutdown_all(self) -> None:
        """Shutdown all agents"""
        for agent in self.agents.values():
            agent.shutdown()
        logger.info("All agents shutdown")


async def main():
    """Main entry point"""
    # Initialize registry
    registry = AgentRegistry()
    
    # Create agents
    researcher = registry.create_agent('researcher')
    analyzer = registry.create_agent('analyzer')
    planner = registry.create_agent('planner')
    executor = registry.create_agent('executor')
    
    logger.info("\n=== Multi-Agent Task Workflow ===")
    
    # Create and execute tasks
    research_task = Task(
        agent_id=researcher.agent_id,
        action='gather_data',
        parameters={'topic': 'AI Trends 2024'}
    )
    
    analyze_task = Task(
        agent_id=analyzer.agent_id,
        action='analyze_data',
        parameters={'data': {}, 'depth': 'detailed'}
    )
    
    planning_task = Task(
        agent_id=planner.agent_id,
        action='create_strategy',
        parameters={'timeline': '3_months'}
    )
    
    execution_task = Task(
        agent_id=executor.agent_id,
        action='implement_plan',
        parameters={'resources': 'allocated'}
    )
    
    # Execute workflow
    for task in [research_task, analyze_task, planning_task, execution_task]:
        result = await registry.execute_task(task)
        logger.info(f"Task {task.task_id}: {result}")
    
    # Display agent statuses
    logger.info("\n=== Agent Status ===")
    statuses = registry.get_all_agents_status()
    for agent_id, status in statuses.items():
        logger.info(f"{agent_id}: {status}")
    
    # Cleanup
    registry.shutdown_all()


if __name__ == "__main__":
    asyncio.run(main())
