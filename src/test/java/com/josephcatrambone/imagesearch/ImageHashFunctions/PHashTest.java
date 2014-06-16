/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.josephcatrambone.imagesearch.ImageHashFunctions;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.util.Random;
import org.junit.After;
import org.junit.AfterClass;
import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

/**
 *
 * @author jcatrambone
 */
public class PHashTest {
	
	public PHashTest() {
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
	 * Test of getHash method, of class PHash.
	 */
	@org.junit.Test
	public void testGetHash() {
		System.out.println("getHash");
		Graphics2D g = null;
		
		// Init our hash function
		PHash instance = new PHash();
		
		// Setup the blank image.
		BufferedImage img = makeBlankImage(128);
		
		// Test blank image
		byte[] expResult = new byte[]{0, 0, 0, 0, 0, 0, 0, 0}; // Blank image should hash to nothing.
		byte[] result = instance.getHash(img);
		System.out.println("result: [" + hashToString(result) + "]");
		//assertArrayEquals(expResult, result);
		
		//assertEquals(expResult, result);
		//fail("The test case is a prototype.");
		
		// Setup a white test image.
		img = makeBlankImage(256, Color.WHITE);
		
		// Test the white image
		expResult = new byte[]{(byte)0xFF, (byte)0xFF, (byte)0xFF, (byte)0xFF, (byte)0xFF, (byte)0xFF, (byte)0xFF, (byte)0xFF};
		result = instance.getHash(img);
		System.out.println("result: [" + hashToString(result) + "]");
		//assertArrayEquals(expResult, result);
		
		// Make an image which is mostly white, except a black patch.
		img = makeBlankImage(256, Color.WHITE);
		g = (Graphics2D)img.getGraphics();
		g.setColor(Color.BLACK);
		g.fillRect(1, 1, 127, 127);
		result = instance.getHash(img);
		System.out.println("result: [" + hashToString(result) + "]");
	}

	/**
	 * Test of getDistance method, of class PHash.
	 */
	@org.junit.Test
	public void testGetDistance() {
		System.out.println("getDistance: Test same image.");
		BufferedImage imgA = makeBlankImage(128);
		BufferedImage imgB = makeBlankImage(128);
		PHash instance = new PHash();
		byte[] hashA = instance.getHash(imgA);
		byte[] hashB = instance.getHash(imgB);
		int expResult = 0;
		int result = instance.getDistance(hashA, hashB);
		assertEquals(expResult, result);
		//fail("The test case is a prototype.");
	}

	/**
	 * Test of getMaxDistance method, of class PHash.
	 */
	@org.junit.Test
	public void testGetMaxDistance() {
		System.out.println("getMaxDistance");
		PHash instance = new PHash();
		float expResult = 64.0F;
		float result = instance.getMaxDistance();
		assertEquals(expResult, result, 0.0);
	}

	/**
	 * Test of getHashName method, of class PHash.
	 */
	@org.junit.Test
	public void testGetHashName() {
		System.out.println("getHashName");
		PHash instance = new PHash();
		String expResult = "pHash";
		String result = instance.getHashName();
		assertEquals(expResult, result);
	}
	
	// Support methods.
	private BufferedImage makeBlankImage(int size) {
		return makeBlankImage(size, Color.BLACK);
	}
	
	private BufferedImage makeBlankImage(int size, Color c) {
		BufferedImage img = new BufferedImage(size, size, BufferedImage.TYPE_INT_ARGB);
		Graphics2D g = (Graphics2D)img.getGraphics(); 
		g.setColor(c);
		g.fillRect(0, 0, size, size);
		return img;
	}
	
	private BufferedImage makeNoiseImage(int size) {
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
	
	private String hashToString(byte[] hash) {
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
