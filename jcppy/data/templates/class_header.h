/**
 * @attention
 * Generated by jccpy {{jcppy_version}}~{{jcppy_revision}}.
 * Do not edit!
 */

#pragma once
#include <iostream>
#include <string>
#include <vector>
#include <cstddef>
#include <stdint.h>


class {{Name}}
{
public:
  {{Name}}();

  static {{Name}} fromJson(const std::string& json);

  static {{Name}} fromJson(const char* json, std::size_t size);

  template<class Iterator>
  static {{Name}} fromJson(Iterator begin, Iterator end);

  template<class Container>
  static {{Name}} fromJson(const Container& container);

  static {{Name}} readJson(std::istream& stream);

  std::string toJson() const;
  std::ostream& writeJson(std::ostream& stream) const;


