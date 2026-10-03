import json
import pytest
from app.tools.calculator import SafeCalculator
from app.llm.prompts import CONDENSE_QUESTION_PROMPT
from app.services.qa_service import QAService
from app.llm.schemas import ChatMessage
from app.db.session import SessionLocal

def test_safe_calculator_tool():
    # Test valid math calculations
    res1 = SafeCalculator.evaluate("500 * 0.18 + 50")
    assert res1["success"] is True
    assert res1["result"] == 140.0

    res2 = SafeCalculator.evaluate("1024 / 8")
    assert res2["success"] is True
    assert res2["result"] == 128.0

    # Test safety / invalid input handling
    res3 = SafeCalculator.evaluate("__import__('os').system('ls')")
    assert res3["success"] is False

def test_multi_turn_query_reformulation_and_tools():
    db = SessionLocal()
    try:
        service = QAService(db)
        
        # Test 1: Direct Tool calling
        calc_result = service.check_and_execute_tools("calculate 250 * 4")
        assert calc_result is not None
        assert "1000" in calc_result

        # Test 2: Multi-turn history reformulation
        history = [
            ChatMessage(role="user", content="What is the refund window?"),
            ChatMessage(role="assistant", content="The refund window is 30 days.")
        ]
        reformulated = service.reformulate_query("Does it apply to digital software?", history)
        assert len(reformulated) > 0
    finally:
        db.close()
