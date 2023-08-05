require "addressable/uri"

uri = Addressable::URI.parse("http://example.com/path/to/resource/")
puts uri.scheme
puts uri.host
puts uri.path
