load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def pull_deps():
    http_archive(
        name = "readline",
        build_file = "@//deps:readline.bzl",
        sha256 = "f8ceb4ee131e3232226a17f51b164afc46cd0b9e6cef344be87c65962cb82b02",
        urls = ["https://ftp.gnu.org/gnu/readline/readline-8.1.tar.gz"],
        strip_prefix = "readline-8.1/",
        patch_cmds = [
            "./configure",
        ],
    )
