# Commercial brief: policy assurance for AI coding-agent adoption

I would use this research to earn a technical discovery conversation, qualify a specific control problem and agree an evidence-based evaluation. It is an account hypothesis, not a pipeline forecast or a claim of product fit.

## Ideal customer profile and buyer personas

My initial ICP hypothesis is an enterprise with substantial software delivery, demonstrated coding-agent adoption, explicit security requirements and a team accountable for enforcing them. Financial services is the focus of this sample, not a claim that the category is limited to that sector.

| Persona | Likely responsibility to qualify | Evidence I would seek |
| --- | --- | --- |
| AppSec / product security leader | Technical champion for software-policy controls | Critical rules, existing coverage, exceptions and investigation effort |
| Engineering / developer platform leader | Operational co-owner and adoption partner | Agent workflows, integration constraints and acceptable developer friction |
| CISO / security executive | Potential sponsor and risk owner | Business impact, assurance requirements and budget ownership |

These are role hypotheses; I have not identified account-specific buyers or confirmed decision authority. Risk, assurance and procurement become stakeholders if discovery establishes a relevant need.

## Priority accounts and buying signals

I would research the following accounts first, in this qualitative order. The order reflects signal specificity and a possible discovery angle, not an automated score or confirmed purchase intent. Public-source claims were rechecked on 1 November 2026; saved scanner observations remain unchanged in [evidence.csv](evidence.csv).

| Priority | Source-reported fact and date | Why I would investigate | Hypothesis to validate |
| --- | --- | --- | --- |
| 1. Monzo | [Building Agent Chip](https://monzo.com/blog/building-agent-chip), published **13 August 2026**, describes regular coding-agent use by nearly all engineers and an internally built platform. | A concrete engineering workflow creates a specific control conversation. The article already describes isolation and access controls. | Could independent evaluation or evidence complement its existing controls? Its internal platform may already meet the need. |
| 2. Barclays | [Anthropic announcement](https://www.anthropic.com/news/barclays-scales-claude), published **1 October 2026**, describes a Claude Code rollout targeting 50% of developers by end-2026. | A stated expansion provides a timely reason to ask about rollout criteria. This is a vendor announcement and a forward-looking target. | Who owns assurance during expansion, and is a control requirement currently unmet? |
| 3. NatWest | [Technology article](https://www.natwestgroup.com/news-and-insights/latest-stories/ai-and-data/2026/feb/being-a-trusted-partner-for-tomorrows-banking-through-technology.html) reports more than 12,000 coders using AI and about 35% of code being AI-written. **Publication date not verified.** | Scale supports a conversation about software-delivery controls; it does not establish agent autonomy. | Which tools act autonomously, which actions require approval, and how is policy compliance evidenced? |

The public Monzo page supplies its date; the original extractor left that field blank. NatWest's URL path is not sufficient to establish a publication date. No historical CSV date or review status has been backfilled.

Barclays and Monzo provide coding-agent-specific context. NatWest's saved excerpt establishes AI-assisted development, not an independently verified deployment of a named autonomous coding tool. Source statements are confirmed as published claims, not independently audited operating metrics.

Revolut and Man Group remain research targets. No curated adoption evidence was captured for them in this exercise. No security-specific hiring signal or security-tool budget was verified for any of the five accounts.

## Confirmed evidence versus commercial hypotheses

The [local policy trial](experiment/policy_test/RESULTS.md) records a completed configuration change despite a conflicting policy, followed by detection. It does not establish a vulnerability at any prospect account.

I would validate whether the account has comparable policy-sensitive workflows, whether existing review and CI already provide sufficient coverage, and whether the buyer values runtime prevention, investigation evidence or release gating. I have not confirmed unmet need, budget, urgency, procurement eligibility or a willingness to buy.

## Five discovery questions

1. Which security requirements must remain true even when an authorised developer requests an exception for debugging?
2. Where do coding agents act today, and which controls evaluate the resulting change rather than just the tool's permission to run?
3. For a disputed change, can your team reconstruct the request, action, policy decision and outcome without relying solely on the agent's explanation?
4. Which actions must be stopped before execution, and where are post-edit detection or release gates sufficient? What happens if a control times out?
5. Who owns a joint security-and-engineering evaluation, and what would count as improved assurance without unacceptable delivery friction?

## Outreach angle and initial sales motion

My opening would use the account's own engineering statement and a question, rather than a claim that its controls have failed:

> Your published engineering work provides a useful starting point for discussing coding-agent oversight. How do your teams distinguish permission to make a change from compliance with the security requirements that change must preserve?

I would tailor the follow-up to the account: complementing an internal platform at Monzo, assurance during rollout at Barclays, or clarifying workflows and ownership at NatWest. This is proposed outreach; no messages have been sent.

My initial motion would be to establish the workflow and control owner, map existing safeguards, then agree one policy and a fictional replay with security and engineering together. Evaluation criteria would include whether an action was observed or intercepted, policy accuracy, failure handling, evidence integrity, integration scope and developer friction. Success measures and any economic case would be agreed with the buyer, not invented from this demo. If current controls already meet the requirement, I would disqualify that use case.

## Relevance to Watcher's category

A category focused on coding-agent oversight can be evaluated against these requirements. I would verify Apollo Watcher's actual tool coverage, deployment model, data handling and enforcement behaviour before proposing a product evaluation. Watcher was not used here; no preventive, integration or compliance capability is assumed.
