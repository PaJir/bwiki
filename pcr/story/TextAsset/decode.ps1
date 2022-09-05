$list = Dir .\*.bytes
foreach ($element in $list) {
	.\story_decode_raw.exe $element
}