/* hamming.c
 * A distance function for PostgreSQL
 * Written by Joseph Catrambone
 * License: 
 * Permissive Coffeware License - A Beerware Derivative.  
 * I say this works, but I'm not responsible if things don't go as planned.
 * If you make anything with this, it would be nice to get credit, but it's not required.
 * If we meet in a coffee shop, it would be nice if you bought me a coffee or a muffin, but that's not required.
 * You are free to modify this as you see fit.  Derivative works do not need to be coffeeware.
 
 * To build:
 * gcc -I`pg_config --includedir` -fpic -c hamming.c
 * gcc -shared -o hamming.so hamming.o
 * sudo cp hamming.so /usr/lib/postgresql/9.1/lib/
 * cd /usr/lib/postgresql/9.1/lib/
 * sudo chmod +r hamming.so

 * To add to Postgres:
 * CREATE FUNCTION HAMMING_DISTANCE(bytea, bytea) RETURNS integer
 * 	AS 'hamming.so', 'HAMMING_DISTANCE'
 * 	LANGUAGE C STRICT;
 */

#include <postgres.h>
#include <fmgr.h>
// On Ubuntu 12.04, I have problems with finding fmgr.  You can include this instead of the line above.
//#include "/usr/include/postgresql/9.1/server/fmgr.h"

#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif

PG_FUNCTION_INFO_V1(HAMMING_DISTANCE);

Datum HAMMING_DISTANCE(PG_FUNCTION_ARGS)
{
	//text *arg1 = PG_GETARG_TEXT_P(0);
	//text *arg2 = PG_GETARG_TEXT_P(1);
	bytea* data1 = PG_GETARG_BYTEA_P(0);
	bytea* data2 = PG_GETARG_BYTEA_P(1);
	int32 num_bytes = VARSIZE(data1) - VARHDRSZ; // VARHDRSZ is the overhead of storage.  Usually sizeof(int4);
	int32 dist = 0;
	int32 index = 0;
	char xor;
	char* st1 = (char*)data1;
	char* st2 = (char*)data2;

	for(index=0; index < 512; ++index) { // TODO: 512 should be num_bytes, just as soon as I can figure out why it's not working.
		// Unroll loop internally
		xor = st1[index] ^ st2[index];
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
	}

    PG_RETURN_INT32(dist);
}
