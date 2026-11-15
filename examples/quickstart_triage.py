"""Quickstart example: classify GitHub issue SLA priority and build LLM context."""

from datetime import UTC, datetime, timedelta

from community_autopilot.core import Analyzer, Comment, Issue, IssueState, Settings


def main() -> None:
    settings = Settings(github_token="demo-token", nemesis_api_key="demo-key")
    analyzer = Analyzer(settings)
    now = datetime.now(UTC)

    issue = Issue(
        repo="benni-os/mcp-forge",
        number=101,
        title="Add WebSocket transport support",
        body="Would love to see WebSocket transport in mcp-forge.",
        author="community-dev",
        state=IssueState.OPEN,
        labels=["enhancement"],
        assignees=[],
        created_at=now - timedelta(hours=36),
        updated_at=now - timedelta(hours=30),
        html_url="https://github.com/benni-os/mcp-forge/issues/101",
        comments=[
            Comment(
                id=1,
                author="community-dev",
                body="Happy to open a PR if this aligns with the roadmap!",
                created_at=now - timedelta(hours=30),
                html_url="https://github.com/benni-os/mcp-forge/issues/101#issuecomment-1",
                is_maintainer=False,
            )
        ],
    )
    priority = analyzer.prioritize(issue)
    context = analyzer.build_context(issue)
    print(f"Issue #{issue.number} Priority: {priority.value}")
    print(f"Context length: {len(context)} chars")


if __name__ == "__main__":
    main()
