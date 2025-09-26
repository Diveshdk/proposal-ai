from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from analysis import DAOAnalyzer

class AnalysisRequest(Model):
    proposal_text: str

class AnalysisResponse(Model):
    report: dict

agent = Agent(name="dao_analyzer", seed="your_seed_phrase_here")
fund_agent_if_low(agent.wallet.address())

analyzer = DAOAnalyzer()

@agent.on_message(AnalysisRequest, replies={AnalysisResponse})
async def analyze_proposal(ctx: Context, sender: str, msg: AnalysisRequest):
    report = analyzer.generate_report(msg.proposal_text)
    await ctx.send(sender, AnalysisResponse(report=report))