
#import re
#testString="'I'\''m a s@f\"  \"e $\\tring w       hich ends in newline\n!!!'"
#re.sub("(!|\$|#|&|\"|\'|\(|\)|\||<|>| |`|\\\|;)", r"\\\1", testString )
#SLASH_ORD = 92
#need_escaped_char = [' ', '!', '"', '#', '$', '&', "'", '(', ')', '*', ',', ';', '<', '>', '?', '[', '\\', ']', '^', '`', '{', '|', '}']
#need_escaped_ords = [32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 44, 59, 60, 62, 63, 91, 92, 93, 94, 96, 123, 124, 125]


def escape( wString ):
	wString = wString.replace( chr( 92 ) , ( chr( 92 ) + chr( 92 ) ) ) # Back Slash ( has to be first )
	wString = wString.replace( chr( 32 ) , ( chr( 92 ) + chr( 32 ) ) ) # space
	wString = wString.replace( "!" , ( chr( 92 ) + "!" ) )
	wString = wString.replace( chr( 34 ) , ( chr( 92 ) + chr( 34 ) ) ) # Double Quote
	wString = wString.replace( "#" , ( chr( 92 ) + "#" ) )
	wString = wString.replace( "$" , ( chr( 92 ) + "$" ) )
	wString = wString.replace( "&" , ( chr( 92 ) + "&" ) )
	wString = wString.replace( chr( 39 ) , ( chr( 92 ) + chr( 39 ) ) ) # Single Quote
	wString = wString.replace( "(" , ( chr( 92 ) + "(" ) )
	wString = wString.replace( ")" , ( chr( 92 ) + ")" ) )
	wString = wString.replace( "*" , ( chr( 92 ) + "*" ) )
	wString = wString.replace( "," , ( chr( 92 ) + "," ) )
	wString = wString.replace( ";" , ( chr( 92 ) + ";" ) )
	wString = wString.replace( "<" , ( chr( 92 ) + "<" ) )
	wString = wString.replace( ">" , ( chr( 92 ) + ">" ) )
	wString = wString.replace( "?" , ( chr( 92 ) + "?" ) )
	wString = wString.replace( "[" , ( chr( 92 ) + "[" ) )
	wString = wString.replace( "]" , ( chr( 92 ) + "]" ) )
	wString = wString.replace( "^" , ( chr( 92 ) + "^" ) )
	wString = wString.replace( "`" , ( chr( 92 ) + "`" ) )
	wString = wString.replace( "{" , ( chr( 92 ) + "{" ) )
	wString = wString.replace( "|" , ( chr( 92 ) + "|" ) )
	wString = wString.replace( "{" , ( chr( 92 ) + "}" ) )
	return wString

if __name__ == "__main__":
	import sys
	print( escape( sys.argv[ 1 ] ) )