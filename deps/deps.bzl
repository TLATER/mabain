load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _patch_readline(repository_ctx):
    pass

http_archive(
    name = "readline",
    build_file = "@//dependency-buildfiles:readline.BUILD",
    sha256 = "f8ceb4ee131e3232226a17f51b164afc46cd0b9e6cef344be87c65962cb82b02",
    urls = ["https://ftp.gnu.org/gnu/readline/readline-8.1.tar.gz"],
)

readline_src = repository_rule(
    implementation = _patch_readline,
    attrs = {
        "readline-src": attr.label_list(allow_files = True),
    },
)
