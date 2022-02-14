cc_library(
    name = "readline",
    srcs = glob([
        "*.c",
        "*.h",
    ]),
    includes = [
        ".",
    ],
    visibility = ["//visibility:public"],
)
