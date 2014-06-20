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

package com.josephcatrambone.imagesearch;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.SpringApplication;


/**
 *
 * @author jcatrambone
 */
@ComponentScan
@EnableAutoConfiguration
public class MainApplication {
	public static void main(String[] args) {
		System.out.println("Starting main...");
		SpringApplication.run(MainApplication.class, args);
	}
}
