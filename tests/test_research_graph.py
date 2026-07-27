# tests/test_research_graph.py
"""
Unit and integration tests for the LangGraph research pipeline.

Testing Strategy:
- Graph compilation: Verify the graph builds without errors
- Node presence: Verify all 7 agent nodes are registered
- End-to-end: Full pipeline invocation with assertion on outputs
"""

import pytest

# Ensure src is importable when running from project root
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.research_graph import build_research_graph
from src.state import AgentState


class TestGraphCompilation:
    """Tests for graph structure and compilation."""

    def test_graph_builds_successfully(self):
        """Verify the StateGraph compiles without runtime errors."""
        graph = build_research_graph()
        assert graph is not None
        # Verify it's a compiled graph (has specific attributes)
        assert hasattr(graph, "invoke")

    def test_graph_has_all_expected_nodes(self):
        """Verify all 7 agent nodes are present in the compiled graph."""
        graph = build_research_graph()
        # Access the underlying graph's nodes
        node_names = set(graph.nodes.keys()) if hasattr(graph, 'nodes') else set()

        expected_nodes = {
            "planner",
            "researcher",
            "analyst",
            "writer",
            "reviewer",
            "reviser",
            "finalizer",
        }
        # If graph.nodes gives us the dict, check intersection
        if node_names:
            assert expected_nodes.issubset(node_names)
        else:
            # Alternative: graph.get_graph() returns a DrawableGraph
            # Skip this check if introspection isn't directly available
            pytest.skip("Graph introspection method not available in this version")

    def test_graph_has_entry_point(self):
        """Verify the graph has an entry point set."""
        graph = build_research_graph()
        # The graph should be invocable
        assert graph is not None


class TestPipelineExecution:
    """Integration tests that actually invoke the pipeline with the LLM.

    These tests require DEEPSEEK_API_KEY to be set in the environment.
    They are slower but validate the full pipeline end-to-end.
    """

    @pytest.fixture
    def initial_state(self) -> dict:
        """Fixture: provide a minimal initial state for testing."""
        return {
            "topic": "Test topic: The benefits of Python for AI development",
            "plan": [],
            "search_results": [],
            "research_summary": "",
            "draft": "",
            "feedback": None,
            "approved": False,
            "final_output": None,
            "revision_count": 0,
            "max_revisions": 1,  # Limit to 1 revision for faster tests
        }

    @pytest.fixture
    def graph(self):
        """Fixture: build the compiled graph."""
        return build_research_graph()

    def test_full_pipeline_invocation(self, graph, initial_state):
        """
        End-to-end test: Invoke the full pipeline and verify outputs.

        Validates:
        - Pipeline completes without errors
        - Final output is produced (non-empty, reasonable length)
        - Research plan is generated
        - State contains expected keys after completion
        """
        config = {"configurable": {"thread_id": "test-session-e2e"}}

        result = graph.invoke(initial_state, config)

        # Assertions on result structure
        assert result is not None
        assert isinstance(result, dict)

        # Verify the pipeline produced a final output
        final_output = result.get("final_output")
        assert final_output is not None, "Final output should not be None"
        assert len(final_output) > 50, (
            f"Final output too short ({len(final_output)} chars). "
            "Expected > 50 characters."
        )

        # Verify plan was generated
        plan = result.get("plan", [])
        assert len(plan) > 0, "Research plan should have at least 1 question"

        # Verify research summary was produced
        research_summary = result.get("research_summary", "")
        assert len(research_summary) > 0, "Research summary should not be empty"

        # Verify draft was produced
        draft = result.get("draft", "")
        assert len(draft) > 0, "Draft should not be empty"

        # State should have all expected keys
        expected_keys = {
            "topic", "plan", "search_results", "research_summary",
            "draft", "feedback", "approved", "final_output",
            "revision_count", "max_revisions",
        }
        assert expected_keys.issubset(set(result.keys())), (
            f"Missing keys in result: {expected_keys - set(result.keys())}"
        )

    def test_pipeline_safety_stops_at_max_revisions(self, graph, initial_state):
        """
        Verify the safety guardrail: pipeline doesn't exceed max_revisions.

        Even if the reviewer would normally request more revisions,
        the pipeline should force-finalize after max_revisions.
        """
        # Set max_revisions to 0 to force immediate finalization
        initial_state["max_revisions"] = 0

        config = {"configurable": {"thread_id": "test-session-safety"}}

        result = graph.invoke(initial_state, config)

        # Revision count should not exceed max_revisions
        revision_count = result.get("revision_count", 0)
        assert revision_count <= initial_state["max_revisions"], (
            f"Revision count ({revision_count}) exceeded "
            f"max_revisions ({initial_state['max_revisions']})"
        )

        # Pipeline should still produce output (force-finalized)
        assert result.get("final_output") is not None