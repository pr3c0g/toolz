#!/usr/bin/env bash

# Ansi coloring functions
print_error() {
  printf "${color_red}${color_bold}"
  printf "$1\n"
  printf "${color_reset}"
}
print_warning() {
  printf "${color_yellow}${color_bold}"
  printf "$1\n"
  printf "${color_reset}"
}
print_success() {
  printf "${color_green}${color_bold}"
  printf "$1\n"
  printf "${color_reset}"
}
print_soft_success() {
  printf "${color_green}"
  printf "$1\n"
  printf "${color_reset}"
}
print_info() {
  printf "${color_blue}"
  printf "$1\n"
  printf "${color_reset}"
}
