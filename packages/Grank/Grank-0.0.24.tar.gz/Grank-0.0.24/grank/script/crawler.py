from ..libs import query
from ..libs import helpers
import click
import pandas as pd
import numpy as np
import click


def fetch_repo_data(owner, repository, config):
    click.echo("========= Crawler start =========")
    # 定义空白数组
    commitArray = []
    pullRequestArray = []

    # 添加一个可过滤掉的数据，确保后续执行完成
    commitArray.append({
        'author': 'localhost',
        'domain': '',
        'is_corp': False,
        'date': '未标注时间',
        "times": 1
    })
    pullRequestArray.append({
        'date': '未标注时间',
        "times": 1
    })
    # 定义查询变量
    start_time = config["time"]["start_time"]
    end_time = config["time"]["end_time"]
    top_number = int(config["rank"]["top"])
    click.echo("第 1 次抓取数据:%s/%s" % (owner, repository))
    # 进行初次查询
    all_query = query.all_query % (owner, repository)
    result = helpers.query(all_query, config)

    # 处理第一组数据
    if (helpers.has_result(result, "commit")):
        for commit in result["data"]["repository"]["ref"]["target"]["history"]["edges"]:
            helpers.add_item_to_commit_array(commit, commitArray)
            pass

    if (helpers.has_result(result, "pr")):
        for pullRequest in result["data"]["repository"]["pullRequests"]["nodes"]:
            helpers.add_item_to_pr_array(pullRequest, pullRequestArray)
    fetch_count = 2
    while helpers.has_next_page(result, "commit") or helpers.has_next_page(result, "issue") or helpers.has_next_page(result, "pr"):
        click.echo("第 %d 次抓取数据:%s/%s" % (fetch_count,owner, repository))
        if (helpers.has_result(result, "commit")):
            for commit in result["data"]["repository"]["ref"]["target"]["history"]["edges"]:
                helpers.add_item_to_commit_array(commit, commitArray)
                pass
        if (helpers.has_result(result, "pr")):
            for pullRequest in result["data"]["repository"]["pullRequests"]["nodes"]:
                helpers.add_item_to_pr_array(pullRequest, pullRequestArray)

        if (helpers.has_next_page(result, "pr") and helpers.has_next_page(result, "commit")):
            next_query = query.all_query_with_pager % (owner, repository, helpers.get_page_cursor(
                result, "pr"), helpers.get_page_cursor(result, "commit"))
        elif (helpers.has_next_page(result, "pr")):
            next_query = query.pr_query_with_pager % (
                owner, repository, helpers.get_page_cursor(result, "pr"))
        elif (helpers.has_next_page(result, "commit")):
            next_query = query.commit_query_with_pager % (
                owner, repository, helpers.get_page_cursor(result, "commit"))

        result = helpers.query(next_query, config)
        fetch_count = fetch_count + 1
    return {
        "pullRequestArray": pullRequestArray,
        "commitArray": commitArray
    }


def fetch_user_data(user, config):
    repositoryArray = []
    click.echo("开始抓取用户数据:%s" % user)
    all_query = query.user_all_query % user
    result = helpers.query(all_query, config)

    if (helpers.has_result(result, 'user_repository')):
        for repo in result["data"]["user"]["repositories"]["nodes"]:
            if repo['stargazers']["totalCount"] > 100 and repo["owner"]["login"].lower() == user.lower():
                repositoryArray.append(
                    {"owner": user, "repository": repo["name"]})

    while(helpers.has_next_page(result, 'user_repository')):
        click.echo("继续抓取用户数据: %s" % user)
        if (helpers.has_result(result, 'user_repository')):
            for repo in result["data"]["user"]["repositories"]["nodes"]:
                if repo['stargazers']["totalCount"] > 100:
                    repositoryArray.append(
                        {"owner": user, "repository": repo["name"]})

        click.echo("继续抓取用户数据: %s" % user)
        next_query = query.user_all_query_with_pager % (
            user, helpers.get_page_cursor(result, "user_repository"))
        result = helpers.query(next_query, config)


    return {
        "repositoryArray": repositoryArray
    }


def fetch_organ_data(organization, config):
    repositoryArray = []
    click.echo("开始抓取组织数据: %s" % organization)
    all_query = query.organ_all_query % organization
    result = helpers.query(all_query, config)
    if (helpers.has_result(result, 'repository')):
        for repo in result["data"]["organization"]["repositories"]["nodes"]:
            if repo['stargazers']["totalCount"] > 100:
                repositoryArray.append(
                    {"owner": organization, "repository": repo["name"]})

    while(helpers.has_next_page(result, 'repository')):
        click.echo("继续抓取组织数据: %s" % organization)
        if (helpers.has_result(result, 'repository')):
            for repo in result["data"]["organization"]["repositories"]["nodes"]:
                if repo['stargazers']["totalCount"] > 100:
                    repositoryArray.append(
                        {"owner": organization, "repository": repo["name"]})

        click.echo("继续抓取组织数据: %s" % organization)
        next_query = query.organ_all_query_with_pager % (
            organization, helpers.get_page_cursor(result, "repository"))
        result = helpers.query(next_query, config)

    return {
        "repositoryArray": repositoryArray
    }
