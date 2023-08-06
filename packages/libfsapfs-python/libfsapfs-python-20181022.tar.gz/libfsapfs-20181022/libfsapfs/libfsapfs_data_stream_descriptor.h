/*
 * The data stream descriptor functions
 *
 * Copyright (C) 2018, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#if !defined( _LIBFSAPFS_DATA_STREAM_DESCRIPTOR_H )
#define _LIBFSAPFS_DATA_STREAM_DESCRIPTOR_H

#include <common.h>
#include <types.h>

#include "libfsapfs_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct libfsapfs_data_stream_descriptor libfsapfs_data_stream_descriptor_t;

struct libfsapfs_data_stream_descriptor
{
	/* The object identifier
	 */
	uint64_t object_identifier;

	/* The physical address
	 */
	uint64_t physical_address;
};

int libfsapfs_data_stream_descriptor_initialize(
     libfsapfs_data_stream_descriptor_t **data_stream_descriptor,
     libcerror_error_t **error );

int libfsapfs_data_stream_descriptor_free(
     libfsapfs_data_stream_descriptor_t **data_stream_descriptor,
     libcerror_error_t **error );

int libfsapfs_data_stream_descriptor_read_data(
     libfsapfs_data_stream_descriptor_t *data_stream_descriptor,
     const uint8_t *data,
     size_t data_size,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBFSAPFS_DATA_STREAM_DESCRIPTOR_H ) */

