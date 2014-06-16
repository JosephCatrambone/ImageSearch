/*
 * Copyright (C) 2014 jcatrambone
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package com.josephcatrambone.imagesearch.ImageHashFunctions;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Random;
import org.junit.After;
import org.junit.AfterClass;
import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

/**
 *
 * @author jcatrambone
 */
@RunWith(Parameterized.class)
public class ImageHashFunctionTest {
	
	@Parameters
	public static Collection<Object[]> data() {
		Collection<Object[]> params = new ArrayList<Object[]>();
		
		BufferedImage exemplarImage = makeBlankImage(256, Color.GRAY);
		BufferedImage[] similarImages = new BufferedImage[2];
		BufferedImage[] differentImages = new BufferedImage[1];
		double threshold = 0.5;
		
		// Make the similar set.
		similarImages[0] = makeBlankImage(256, Color.BLACK);
		similarImages[1] = makeBlankImage(256, Color.WHITE);
		
		// Different set
		differentImages[0] = makeNoiseImage(256);
		
		params.add(new Object[] {SimpleHash.class, exemplarImage, similarImages, differentImages, threshold});
		params.add(new Object[] {PHash.class, exemplarImage, similarImages, differentImages, threshold});
		
		return params;
    }
	
	private ImageHashFunction hashFunction;
	private BufferedImage exemplar; // This is the basis image
	private BufferedImage[] similarSet; // These are similar to the image
	private BufferedImage[] differentSet; // These are different from.
	private double matchThreshold; // The threshold as a function of the max distance.  Similars must be closer than this.  Different must be greater.
	
	public ImageHashFunctionTest(Class hashFunctionClass, BufferedImage exemplar, BufferedImage[] similar, BufferedImage[] different, double threshold) {
		try {
			this.hashFunction = (ImageHashFunction)hashFunctionClass.newInstance();
		} catch(InstantiationException ie) {
			System.err.println("Unable to instantiate ImageHash function " + hashFunctionClass.getName());
			System.err.println(ie);
			fail("Unable to instance test.");
		} catch(IllegalAccessException ie) {
			System.err.println("IllegalAccess exception while instantiating ImageHash function " + hashFunctionClass.getName());
			System.err.println(ie);
			fail("Unable to instance test.");
		}
		this.exemplar = exemplar;
		this.similarSet = similar;
		this.differentSet = different;
		this.matchThreshold = threshold;
	}
	
	@BeforeClass
	public static void setUpClass() {
	}
	
	@AfterClass
	public static void tearDownClass() {
	}
	
	@Before
	public void setUp() {
	}
	
	@After
	public void tearDown() {
	}

	/**
	 * Test of the overall robustness of an algorithm.
	 * Test for invariance to scale, rotation, and translation.
	 */
	@Test
	public void reportRobustness() {
		
	}
	
	/**
	 * Test of getHash method, of class ImageHashFunction.
	 * Tests only the most basic property: identity.
	 */
	@Test
	public void testGetHash() {
		System.out.println("getHash");
		assertArrayEquals(hashFunction.getHash(exemplar), hashFunction.getHash(exemplar));
	}

	/**
	 * Test of getDistance method, of class ImageHashFunction.
	 * Tests the basic properties of the distance function.
	 */
	@Test
	public void testGetDistance() {
		System.out.println("getDistance");
		byte[] hashA = hashFunction.getHash(exemplar);
		byte[] hashB = hashFunction.getHash(similarSet[0]);
		byte[] hashC = hashFunction.getHash(differentSet[0]);
		
		int distAA = hashFunction.getDistance(hashA, hashA);
		int distAB = hashFunction.getDistance(hashA, hashB);
		int distAC = hashFunction.getDistance(hashA, hashC);
		
		assertEquals(distAA, 0);
		assertTrue(distAA < distAB);
		
		//fail("The test case is a prototype.");
	}

	/**
	 * Test of getMaxDistance method, of class ImageHashFunction.
	 */
	@Test
	public void testGetMaxDistance() {
		System.out.println("getMaxDistance");
		float result = hashFunction.getMaxDistance();
		assertTrue(result > 0.0);
	}

	/**
	 * Test of getHashName method, of class ImageHashFunction.
	 */
	@Test
	public void testGetHashName() {
		System.out.println("getHashName");
		String result = hashFunction.getHashName();
		assertNotNull(result);
		assertNotSame(result, "");
	}
	
	private static BufferedImage makeBlankImage(int size, Color c) {
		BufferedImage img = new BufferedImage(size, size, BufferedImage.TYPE_INT_ARGB);
		Graphics2D g = (Graphics2D)img.getGraphics(); 
		g.setColor(c);
		g.fillRect(0, 0, size, size);
		return img;
	}
	
	private static BufferedImage makeNoiseImage(int size) {
		Random random = new Random();
		BufferedImage img = new BufferedImage(size, size, BufferedImage.TYPE_INT_ARGB);
		Graphics2D g = (Graphics2D)img.getGraphics(); 
		for(int y=0; y < size; y++) {
			for(int x=0; x < size; x++) {
				g.setColor(new Color(random.nextFloat(), random.nextFloat(), random.nextFloat()));
				g.drawRect(x, y, 1, 1);
			}
		}
		return img;
	}
	
	private static String hashToString(byte[] hash) {
		char[] s = new char[hash.length*8];
		for(int i=0; i < hash.length; i++) {
			int b = Byte.toUnsignedInt(hash[i]);
			for(int j=0; j < 8; j++) {
				if((b & 0x01) == 1) {
					s[i*8 + j] = '1';
				} else {
					s[i*8 + j] = '0';
				}
				b = b >> 1;
			}
		}
		return new String(s);
	}
}
