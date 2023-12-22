"use client";

import Link from "next/link";
import { ArrowLeftIcon } from "@heroicons/react/24/solid";
import { useRouter } from "next/navigation";

export default function BackLink() {
  const router = useRouter();

  return (
    <Link href="" onClick={() => router.back()} className="flex items-baseline">
      <ArrowLeftIcon className="text-white w-3 h-3 mr-2" />
      back
    </Link>
  );
}
