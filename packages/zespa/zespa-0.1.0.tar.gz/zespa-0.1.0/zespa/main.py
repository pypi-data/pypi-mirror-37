import fire
from beautifultable import BeautifulTable
from tqdm import tqdm

from zespa.configuration import ZespaConfiguration
from zespa.github_requester import GitHubRequester
from zespa.issue import Issue
from zespa.zenhub_requester import ZenHubRequester


class Zespa():
    def __init__(self):
        self._config = ZespaConfiguration()

    def configure(self):
        self._config.create()
        return 'OK'

    def aggregate(self, start_date, end_date, *labels):
        self._config.check()
        repo_name = self._config.get_repo_name()
        github_token = self._config.get_github_token()
        github_requester = GitHubRequester(repo_name, github_token)

        zenhub_token = self._config.get_zenhub_token()
        repo_id = github_requester.get_repo_id()
        zenhub_requester = ZenHubRequester(repo_id, zenhub_token)

        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        aggregation_groups = self._parse_label_args(labels)

        github_issues = github_requester.get_issues(start_date, end_date)
        issue_list = []
        for g_issue in tqdm(github_issues):
            issue = Issue(id=g_issue['number'], labels=[label_info['name'] for label_info in g_issue['labels']])
            issue.estimate = zenhub_requester.get_estimate(issue.id)
            issue_list.append(issue)

        result = self._build_table(aggregation_groups, issue_list)
        print(result)

    def _parse_label_args(self, labels):
        aggregation_groups = []
        index = -1
        for label in labels:
            if label == '--labels':
                aggregation_groups.append([])
                index += 1
            else:
                aggregation_groups[index].append(label)
        return aggregation_groups

    def _build_table(self, aggregation_groups, issue_list):
        table = BeautifulTable()
        results = []
        table.column_headers = [' or '.join(labels) for labels in aggregation_groups]
        for aggregation_group in aggregation_groups:
            group_estimate = 0
            for issue in issue_list:
                for label in issue.labels:
                    if label in aggregation_group:
                        group_estimate += issue.estimate
                        break
                    elif aggregation_group[0].lower() == 'all':
                        group_estimate += issue.estimate
                        break
            results.append(group_estimate)

        table.append_row(results)
        return table


def main():
    fire.Fire(Zespa(), name='zespa')


if __name__ == '__main__':
    main()
