cc_library(
    name = "readline",
    srcs = glob([
        "readline-8.1/*.c",
        "readline-8.1/*.h",
    ]),
    includes = [
        ".",
    ],
    visibility = ["//visibility:public"],
)
