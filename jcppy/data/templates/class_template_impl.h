template<class Iterator>
{{Name}} {{Name}}::fromJson(Iterator begin, Iterator end)
{
  {{Name}}Reader reader;
  reader.read(begin, end);
  return reader.instance();
};

template<class Container>
{{Name}} {{Name}}::fromJson(const Container& container)
{
  return fromJson(container.begin(), container.end());
}


