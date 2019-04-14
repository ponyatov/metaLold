
// line 1 "FORTH.ragel"
package io.github.ponyatov.metal;


// line 7 "FORTH.ragel"


public class FORTH {

	
// line 13 "app/src/main/java//io/github/ponyatov/metal/FORTH.java"
private static byte[] init__lexer_key_offsets_0()
{
	return new byte [] {
	    0,    0,    0
	};
}

private static final byte _lexer_key_offsets[] = init__lexer_key_offsets_0();


private static char[] init__lexer_trans_keys_0()
{
	return new char [] {
	    0
	};
}

private static final char _lexer_trans_keys[] = init__lexer_trans_keys_0();


private static byte[] init__lexer_single_lengths_0()
{
	return new byte [] {
	    0,    0,    0
	};
}

private static final byte _lexer_single_lengths[] = init__lexer_single_lengths_0();


private static byte[] init__lexer_range_lengths_0()
{
	return new byte [] {
	    0,    0,    0
	};
}

private static final byte _lexer_range_lengths[] = init__lexer_range_lengths_0();


private static byte[] init__lexer_index_offsets_0()
{
	return new byte [] {
	    0,    0,    1
	};
}

private static final byte _lexer_index_offsets[] = init__lexer_index_offsets_0();


private static byte[] init__lexer_trans_targs_0()
{
	return new byte [] {
	    2,    0,    0
	};
}

private static final byte _lexer_trans_targs[] = init__lexer_trans_targs_0();


static final int lexer_start = 1;
static final int lexer_first_final = 2;
static final int lexer_error = 0;

static final int lexer_en_main = 1;


// line 12 "FORTH.ragel"
	
	public static void parse(String cmd) throws ParseException {
	
		
// line 86 "app/src/main/java//io/github/ponyatov/metal/FORTH.java"
	{
	int _klen;
	int _trans = 0;
	int _keys;
	int _goto_targ = 0;

	_goto: while (true) {
	switch ( _goto_targ ) {
	case 0:
	if ( p == pe ) {
		_goto_targ = 4;
		continue _goto;
	}
	if ( cs == 0 ) {
		_goto_targ = 5;
		continue _goto;
	}
case 1:
	_match: do {
	_keys = _lexer_key_offsets[cs];
	_trans = _lexer_index_offsets[cs];
	_klen = _lexer_single_lengths[cs];
	if ( _klen > 0 ) {
		int _lower = _keys;
		int _mid;
		int _upper = _keys + _klen - 1;
		while (true) {
			if ( _upper < _lower )
				break;

			_mid = _lower + ((_upper-_lower) >> 1);
			if ( data[p] < _lexer_trans_keys[_mid] )
				_upper = _mid - 1;
			else if ( data[p] > _lexer_trans_keys[_mid] )
				_lower = _mid + 1;
			else {
				_trans += (_mid - _keys);
				break _match;
			}
		}
		_keys += _klen;
		_trans += _klen;
	}

	_klen = _lexer_range_lengths[cs];
	if ( _klen > 0 ) {
		int _lower = _keys;
		int _mid;
		int _upper = _keys + (_klen<<1) - 2;
		while (true) {
			if ( _upper < _lower )
				break;

			_mid = _lower + (((_upper-_lower) >> 1) & ~1);
			if ( data[p] < _lexer_trans_keys[_mid] )
				_upper = _mid - 2;
			else if ( data[p] > _lexer_trans_keys[_mid+1] )
				_lower = _mid + 2;
			else {
				_trans += ((_mid - _keys)>>1);
				break _match;
			}
		}
		_trans += _klen;
	}
	} while (false);

	cs = _lexer_trans_targs[_trans];

case 2:
	if ( cs == 0 ) {
		_goto_targ = 5;
		continue _goto;
	}
	if ( ++p != pe ) {
		_goto_targ = 1;
		continue _goto;
	}
case 4:
case 5:
	}
	break; }
	}

// line 16 "FORTH.ragel"
		
	}
}