package com.josephcatrambone.imagesearch.ImageHashFunctions;

import java.awt.image.BufferedImage;

/** ImageHashFunction
 * Defines the interface for hash functions.
 * @author jcatrambone
 */
public interface ImageHashFunction {
	// Unfortunately, abstract and static are not allowed to modify the same function.
	// We basically need this to be an interface and for sub-interfaces to be classes.
	
	/*** getHash
	 * Takes a buffered image and returns an array of bytes which obey the properties of hashes.
	 * Hash(x) == Hash(y) if x == y.  Hash(x) ^ Hash(y) > 0 as x becomes more different from y. 
	 * @param img The input image.
	 * @return 
	 */
	public byte[] getHash(BufferedImage img);
	
	/*** getDistance
	 * Returns the distance between two hash functions produced by the same function.
	 * @param hashA
	 * @param hashB
	 * @return Larger numbers indicate larger differences in hash.
	 */
	public int getDistance(byte[] hashA, byte[] hashB);
	
	/*** getMaxDistance
	 * Return the largest distance that can be returned by the getDistance function.
	 * May return infinity.  Must return greater than zero.
	 * @return 
	 */
	public float getMaxDistance();
	
	/*** getHashName
	 * Return the name of the hash function.
	 * @return A string with no other guarantees.
	 */
	public String getHashName();
}
