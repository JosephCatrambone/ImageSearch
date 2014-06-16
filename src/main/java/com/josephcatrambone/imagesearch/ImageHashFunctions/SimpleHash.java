/*
 * Copyright (C) 2014 Jospeh Catrambone
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

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;

/**
 *
 * @author jcatrambone
 */
public class SimpleHash implements ImageHashFunction {

	@Override
	public byte[] getHash(BufferedImage img) {
		byte[] hash = new byte[8];
		
		// Convert image
		BufferedImage temp = new BufferedImage(8, 8, BufferedImage.TYPE_BYTE_GRAY);
		Graphics2D g = (Graphics2D)temp.getGraphics();
		g.drawImage(img, 0, 0, 8, 8, 0, 0, img.getWidth(), img.getHeight(), null);
		
		// Compute mean
		double mean = 0;
		for(int y=0; y < temp.getHeight(); y++) {
			for(int x=0; x < temp.getWidth(); x++) {
				mean += (temp.getRGB(x, y)&0x000000FF)/255.0;
			}
		}
		mean /= (double)(img.getWidth()*img.getHeight());
		
		// Calculate hash
		for(int y=0; y < temp.getHeight(); y++) {
			int currentByte = 0;
			for(int x=0; x < temp.getWidth(); x++) {
				if((temp.getRGB(x, y)&0x000000FF)/255.0 > mean) {
					currentByte |= 0x01;
				}
				currentByte = currentByte << 1;
			}
			hash[y] = (byte)currentByte;
		}
		
		return hash;
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
		return 64.0f;
	}

	@Override
	public String getHashName() {
		return "BasicHash";
	}
	
}
