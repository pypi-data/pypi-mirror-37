/*
 * The data stream handle functions
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

#include <common.h>
#include <memory.h>
#include <types.h>

#include "libfsapfs_data_block.h"
#include "libfsapfs_data_stream_handle.h"
#include "libfsapfs_definitions.h"
#include "libfsapfs_libbfio.h"
#include "libfsapfs_libcerror.h"
#include "libfsapfs_libfcache.h"
#include "libfsapfs_libfdata.h"
#include "libfsapfs_unused.h"
#include "libfsapfs_volume_data_handle.h"

/* Creates data stream handle
 * Make sure the value data_stream_handle is referencing, is set to NULL
 * Returns 1 if successful or -1 on error
 */
int libfsapfs_data_stream_handle_initialize(
     libfsapfs_data_stream_handle_t **data_stream_handle,
     libfsapfs_io_handle_t *io_handle,
     libcerror_error_t **error )
{
	libfsapfs_volume_data_handle_t *volume_data_handle = NULL;
	static char *function                              = "libfsapfs_data_stream_handle_initialize";	
	int element_index                                  = 0;

	if( data_stream_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid data stream handle.",
		 function );

		return( -1 );
	}
	if( *data_stream_handle != NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_ALREADY_SET,
		 "%s: invalid data stream handle value already set.",
		 function );

		return( -1 );
	}
	if( io_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid IO handle.",
		 function );

		return( -1 );
	}
	*data_stream_handle = memory_allocate_structure(
	                       libfsapfs_data_stream_handle_t );

	if( *data_stream_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_INSUFFICIENT,
		 "%s: unable to create data stream handle.",
		 function );

		goto on_error;
	}
	if( memory_set(
	     *data_stream_handle,
	     0,
	     sizeof( libfsapfs_data_stream_handle_t ) ) == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_SET_FAILED,
		 "%s: unable to clear data stream handle.",
		 function );

		memory_free(
		 *data_stream_handle );

		*data_stream_handle = NULL;

		return( -1 );
	}
	if( libfsapfs_volume_data_handle_initialize(
	     &volume_data_handle,
	     io_handle,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_INITIALIZE_FAILED,
		 "%s: unable to create volume data handle.",
		 function );

		goto on_error;
	}
	if( libfdata_vector_initialize(
	     &( ( *data_stream_handle )->data_block_vector ),
	     (size64_t) io_handle->block_size,
	     (intptr_t *) volume_data_handle,
	     (int (*)(intptr_t **, libcerror_error_t **)) &libfsapfs_volume_data_handle_free,
	     NULL,
	     (int (*)(intptr_t *, intptr_t *, libfdata_vector_t *, libfdata_cache_t *, int, int, off64_t, size64_t, uint32_t, uint8_t, libcerror_error_t **)) &libfsapfs_volume_data_handle_read_data_block,
	     NULL,
	     LIBFDATA_DATA_HANDLE_FLAG_MANAGED,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_INITIALIZE_FAILED,
		 "%s: unable to create data block vector.",
		 function );

		goto on_error;
	}
	( *data_stream_handle )->volume_data_handle = volume_data_handle;
	volume_data_handle                          = NULL;

	if( libfdata_vector_append_segment(
	     ( *data_stream_handle )->data_block_vector,
	     &element_index,
	     0,
	     0,
	     io_handle->container_size,
	     0,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_APPEND_FAILED,
		 "%s: unable to append segment to data block vector.",
		 function );

		goto on_error;
	}
	if( libfcache_cache_initialize(
	     &( ( *data_stream_handle )->data_block_cache ),
	     LIBFSAPFS_MAXIMUM_CACHE_ENTRIES_DATA_BLOCKS,
	     error ) != 1 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_INITIALIZE_FAILED,
		 "%s: unable to create data block cache.",
		 function );

		goto on_error;
	}
	( *data_stream_handle )->io_handle = io_handle;

	return( 1 );

on_error:
	if( *data_stream_handle != NULL )
	{
		if( ( *data_stream_handle )->data_block_cache != NULL )
		{
			libfcache_cache_free(
			 &( ( *data_stream_handle )->data_block_cache ),
			 NULL );
		}
		if( ( *data_stream_handle )->data_block_vector != NULL )
		{
			libfdata_vector_free(
			 &( ( *data_stream_handle )->data_block_vector ),
			 NULL );
		}
		if( volume_data_handle != NULL )
		{
			libfsapfs_volume_data_handle_free(
			 &volume_data_handle,
			 NULL );
		}
		memory_free(
		 *data_stream_handle );

		*data_stream_handle = NULL;
	}
	return( -1 );
}

/* Frees data stream handle
 * Returns 1 if successful or -1 on error
 */
int libfsapfs_data_stream_handle_free(
     libfsapfs_data_stream_handle_t **data_stream_handle,
     libcerror_error_t **error )
{
	static char *function = "libfsapfs_data_stream_handle_free";
	int result            = 1;

	if( data_stream_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid data stream handle.",
		 function );

		return( -1 );
	}
	if( *data_stream_handle != NULL )
	{
		if( libfdata_vector_free(
		     &( ( *data_stream_handle )->data_block_vector ),
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
			 "%s: unable to free data block vector.",
			 function );

			result = -1;
		}
		if( libfcache_cache_free(
		     &( ( *data_stream_handle )->data_block_cache ),
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_FINALIZE_FAILED,
			 "%s: unable to free data block cache.",
			 function );

			result = -1;
		}
		memory_free(
		 *data_stream_handle );

		*data_stream_handle = NULL;
	}
	return( result );
}

/* Reads data from the current offset into a buffer
 * Callback for the data stream
 * Returns the number of bytes read or -1 on error
 */
ssize_t libfsapfs_data_stream_handle_read_segment_data(
         libfsapfs_data_stream_handle_t *data_stream_handle,
         libbfio_handle_t *file_io_handle,
         int segment_index LIBFSAPFS_ATTRIBUTE_UNUSED,
         int segment_file_index LIBFSAPFS_ATTRIBUTE_UNUSED,
         uint8_t *segment_data,
         size_t segment_data_size,
         uint32_t segment_flags LIBFSAPFS_ATTRIBUTE_UNUSED,
         uint8_t read_flags LIBFSAPFS_ATTRIBUTE_UNUSED,
         libcerror_error_t **error )
{
	libfsapfs_data_block_t *data_block = NULL;
	static char *function              = "libfsapfs_data_stream_handle_read_segment_data";
	size_t data_block_offset           = 0;
	size_t segment_data_offset         = 0;
	size_t read_size                   = 0;
	uint64_t block_number              = 0;

	LIBFSAPFS_UNREFERENCED_PARAMETER( segment_index )
	LIBFSAPFS_UNREFERENCED_PARAMETER( segment_file_index )
	LIBFSAPFS_UNREFERENCED_PARAMETER( segment_flags )
	LIBFSAPFS_UNREFERENCED_PARAMETER( read_flags )

	if( data_stream_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid data stream handle.",
		 function );

		return( -1 );
	}
	if( data_stream_handle->io_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_MISSING,
		 "%s: invalid data stream handle - missing IO handle.",
		 function );

		return( -1 );
	}
	if( data_stream_handle->current_segment_offset < 0 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_VALUE_OUT_OF_BOUNDS,
		 "%s: invalid data stream handle - current segment offset value out of bounds.",
		 function );

		return( -1 );
	}
	if( segment_data == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid segment data.",
		 function );

		return( -1 );
	}
	if( segment_data_size > (size_t) SSIZE_MAX )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_VALUE_EXCEEDS_MAXIMUM,
		 "%s: invalid segment data size value exceeds maximum.",
		 function );

		return( -1 );
	}
	block_number      = data_stream_handle->current_segment_offset / data_stream_handle->io_handle->block_size;
	data_block_offset = data_stream_handle->current_segment_offset % data_stream_handle->io_handle->block_size;

	while( segment_data_size > 0 )
	{
		if( libfdata_vector_get_element_value_by_index(
		     data_stream_handle->data_block_vector,
		     (intptr_t *) file_io_handle,
		     (libfdata_cache_t *) data_stream_handle->data_block_cache,
		     block_number,
		     (intptr_t **) &data_block,
		     0,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_GET_FAILED,
			 "%s: unable to retrieve data block: %" PRIu64 ".",
			 function,
			 block_number );

			return( -1 );
		}
		if( data_block == NULL )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_VALUE_MISSING,
			 "%s: invalid data block: %" PRIu64 ".",
			 function,
			 block_number );

			return( -1 );
		}
		if( data_block->data == NULL )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_VALUE_MISSING,
			 "%s: invalid data block: %" PRIu64 " - missing data.",
			 function,
			 block_number );

			return( -1 );
		}
		if( segment_data_size < data_stream_handle->io_handle->block_size )
		{
			read_size = segment_data_size;
		}
		else
		{
			read_size = (size_t) ( data_stream_handle->io_handle->block_size - data_block_offset );
		}
		if( ( read_size > data_block->data_size )
		 || ( data_block_offset > ( data_block->data_size - read_size ) ) )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_VALUE_OUT_OF_BOUNDS,
			 "%s: invalid read size value out of bounds.",
			 function );

			return( -1 );
		}
		if( memory_copy(
		     &( segment_data[ segment_data_offset ] ),
		     &( data_block->data[ data_block_offset ] ),
		     read_size ) == NULL )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_MEMORY,
			 LIBCERROR_MEMORY_ERROR_COPY_FAILED,
			 "%s: unable to copy data block: %" PRIu64 " data.",
			 function,
			 block_number );

			return( -1 );
		}
		data_block_offset    = 0;
		segment_data_offset += read_size;
		segment_data_size   -= read_size;

		block_number++;
	}
	return( (ssize_t) segment_data_offset );
}

/* Seeks a certain offset of the data
 * Callback for the data stream
 * Returns the offset if seek is successful or -1 on error
 */
off64_t libfsapfs_data_stream_handle_seek_segment_offset(
         libfsapfs_data_stream_handle_t *data_stream_handle,
         intptr_t *file_io_handle LIBFSAPFS_ATTRIBUTE_UNUSED,
         int segment_index LIBFSAPFS_ATTRIBUTE_UNUSED,
         int segment_file_index LIBFSAPFS_ATTRIBUTE_UNUSED,
         off64_t segment_offset,
         libcerror_error_t **error )
{
	static char *function = "libfsapfs_data_stream_handle_seek_segment_offset";

	LIBFSAPFS_UNREFERENCED_PARAMETER( file_io_handle )
	LIBFSAPFS_UNREFERENCED_PARAMETER( segment_index )
	LIBFSAPFS_UNREFERENCED_PARAMETER( segment_file_index )

	if( data_stream_handle == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid data stream handle.",
		 function );

		return( -1 );
	}
	if( segment_offset < 0 )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_VALUE_OUT_OF_BOUNDS,
		 "%s: invalid segment offset value out of bounds.",
		 function );

		return( -1 );
	}
	data_stream_handle->current_segment_offset = segment_offset;

	return( segment_offset );
}

