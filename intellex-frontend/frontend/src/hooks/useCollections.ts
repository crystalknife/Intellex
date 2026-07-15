"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  addToCollection,
  createCollection,
  deleteCollection,
  getCollection,
  getCollections,
  removeFromCollection,
  renameCollection,
} from "@/lib/api";

const COLLECTIONS_KEY = ["collections"] as const;
const collectionKey = (id: string) => ["collections", id] as const;

export function useCollections() {
  return useQuery({
    queryKey: COLLECTIONS_KEY,
    queryFn: getCollections,
    staleTime: 30_000,
  });
}

export function useCollection(id: string) {
  return useQuery({
    queryKey: collectionKey(id),
    queryFn: () => getCollection(id),
    enabled: Boolean(id),
    staleTime: 15_000,
  });
}

export function useCreateCollection() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (name: string) => createCollection(name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: COLLECTIONS_KEY });
    },
  });
}

export function useRenameCollection() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, name }: { id: string; name: string }) =>
      renameCollection(id, name),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: COLLECTIONS_KEY });
      queryClient.invalidateQueries({ queryKey: collectionKey(variables.id) });
    },
  });
}

export function useDeleteCollection() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => deleteCollection(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: COLLECTIONS_KEY });
    },
  });
}

export function useAddToCollection() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      collectionId,
      type,
      itemId,
    }: {
      collectionId: string;
      type: "document" | "event";
      itemId: string;
    }) => addToCollection(collectionId, type, itemId),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: COLLECTIONS_KEY });
      queryClient.invalidateQueries({
        queryKey: collectionKey(variables.collectionId),
      });
    },
  });
}

export function useRemoveFromCollection() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      collectionId,
      itemId,
    }: {
      collectionId: string;
      itemId: string;
    }) => removeFromCollection(collectionId, itemId),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: COLLECTIONS_KEY });
      queryClient.invalidateQueries({
        queryKey: collectionKey(variables.collectionId),
      });
    },
  });
}
