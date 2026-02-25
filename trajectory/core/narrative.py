class NarrativeEngine:
    SURGEON_STORY = [
        "DAY 1: ROUTINE CASES. Your surgical career begins at City Hospital. Stabilize three patients with routine bypass procedures.",
        "DAY 2: FIRST COMPLICATION. An unexpected valve issue is discovered mid-surgery. The anesthesiologist signals a warning.",
        "DAY 3: RISING TENSION. High-risk cases are piling up. Hospital administration is pressuring for faster throughput.",
        "DAY 4: THE CRISIS. A critical trauma case arrives during a regional blood shortage. Every second counts.",
        "DAY 5: RESOLUTION. Your final performance today determines your medical legacy. High reputation opens elective surgery windows."
    ]

    TRADER_STORY = [
        "DAY 1: MARKET OPEN. You've been allocated $487k. Start by analyzing asset momentum and establishing core positions.",
        "DAY 2: EARLY GAINS. Portfolio is up. HFT algorithms are becoming active, competing for your entry levels.",
        "DAY 3: VOLATILITY SPIKE. A sudden Fed announcement sends ripples through the tech sector. Hedge or hold?",
        "DAY 4: THE DOWNTURN. Market liquidity is drying up. A major institutional whale is liquidating heavy positions.",
        "DAY 5: ENDGAME. Closing bell approaches. Optimize your exit strategy to maximize final P&L."
    ]

    def get_day_text(self, career, day):
        # day is 0-4
        if "Surgeon" in career or "Doctor" in career:
            return self.SURGEON_STORY[min(day, 4)]
        elif "Trader" in career:
            return self.TRADER_STORY[min(day, 4)]
        return f"DAY {day+1}: Professional progression in {career}."
