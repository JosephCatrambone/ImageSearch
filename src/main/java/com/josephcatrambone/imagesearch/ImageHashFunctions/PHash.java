/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.josephcatrambone.imagesearch.ImageHashFunctions;

import java.awt.image.BufferedImage;

/**
 *
 * @author jcatrambone
 */
public class PHash implements ImageHashFunction {
	
	@Override
	public byte[] getHash(BufferedImage img) {
		// Perform a DCT hash of the specified image.
		byte[] output = new byte[8];
		double[] result = new double[32*32];
		
		// Scale the image to 32x32 and make it greyscale
		BufferedImage tempImg = new BufferedImage(32, 32, BufferedImage.TYPE_BYTE_GRAY);
		tempImg.getGraphics().drawImage(img, 0, 0, 32, 32, 0, 0, img.getWidth(), img.getHeight(), null);
		
		// Compute the DCT
		/*
		for(int y=0; y < tempImg.getHeight(); y++) {
			for(int x=0; x < tempImg.getWidth(); x++) {
				result[y * tempImg.getWidth() + x] = 0;
				for(int v=0; v < tempImg.getHeight(); v++) {
					for(int u=0; u < tempImg.getWidth(); u++) {
						result[y*tempImg.getWidth()+x] += alpha(u)*alpha(v)*tempImg.getRGB(u, v)*altcos(u,x)*altcos(v,y);
					}
				}
			}
		}
		*/
		for(int y=0; y < tempImg.getHeight(); y++) {
			for(int x=0; x < tempImg.getWidth(); x++) {
				result[y*tempImg.getWidth() + x] = 0;
				for(int v=0; v < tempImg.getHeight(); v++) {
					for(int u=0; u < tempImg.getWidth(); u++) {
						result[y*tempImg.getWidth()+x] += tempImg.getRGB(u, v) * Math.cos(Math.PI/((float)tempImg.getHeight())*(v+1.0/2.0)*y) * Math.cos(Math.PI/((float)tempImg.getWidth())*(u+1.0/2.0)*x);
					}
				}
			}
		}
		
		// Calculate the mean
		double mean = 0;
		for(int i=0; i < result.length; i++) {
			mean += result[i];
		}
		mean /= result.length;
		
		// Produce the actual hash.
		for(int i=0; i < 8; i++) { // 8 bits in a byte, last time I checked.
			byte val = 0;
			for(int j=0; j < 8; j++) { // And we only care about the top 8x8 space.
				if(result[i + j*tempImg.getWidth()] > mean) { 
					val |= 0x01;
				}
				val = (byte)(val << 1);
			}
			output[i] = val;
		}
		
		return output;
	}

	@Override
	public int getDistance(byte[] hashA, byte[] hashB) {
		int distance = 0;
		for(int i=0; i < hashA.length; i++) {
			int a = Byte.toUnsignedInt(hashA[i]);
			int b = Byte.toUnsignedInt(hashB[i]);
			for(int j=0; j < 8; j++) {
				if((a&0x01) != (b&0x01)) {
					distance += 1;
				}
				a = a / 2;
				b = b / 2;
			}
		}
		return distance;
	}

	@Override
	public float getMaxDistance() {
		return 64f;
	}

	@Override
	public String getHashName() {
		return "pHash";
	}
	
	private static double alpha(float d) {
		if(d == 0) {
			return Math.sqrt(2)*0.25; // sqrt(2)/2/2;
		}
		return 0.5;
	}
	
	private static double altcos(float a, float b) {
		return Math.cos(Math.PI * a * (2.0*b+1) * (1.0/16));
	}
	
	public long hashToInteger(byte[] hash) {
		long i = 0;
		for(int a = 0; a < hash.length*8; a++) {
			int byteIndex = a/8;
			int bitIndex = a%8;
			if((hash[byteIndex] & (0x01 << bitIndex)) > 0) {
				i |= 0x01;
			}
			i = i << 1;
		}
		return i;
	}
}
