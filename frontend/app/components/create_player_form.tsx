"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useForm } from "react-hook-form";

const CreatePlayerFormSchema = z.object({
  firstName: z
    .string()
    .min(1, { message: "First name is required" })
    .max(50, { message: "First name must be less than 50 characters" }),
  lastName: z
    .string()
    .min(1, { message: "Last name is required" })
    .max(50, { message: "Last name must be less than 50 characters" }),
});

const CreatePlayerForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(CreatePlayerFormSchema) });
  return (
    <form
      onSubmit={handleSubmit((data) => console.log(data))}
      className="flex w-full max-w-md flex-col gap-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-lg sm:p-8"
    >
      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Add a player
        </h1>
        <p className="text-sm text-slate-600">
          Enter the player&apos;s name to add them to your roster.
        </p>
      </header>
      <div className="flex flex-col gap-2">
        <label htmlFor="firstName" className="text-sm font-medium text-slate-700">
          First name
        </label>
        <input
          id="firstName"
          autoComplete="given-name"
          {...register("firstName")}
          aria-invalid={!!errors.firstName}
          aria-describedby={errors.firstName ? "firstName-error" : undefined}
          className="rounded-lg border border-slate-300 px-3 py-2.5 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20"
          placeholder="e.g. Alex"
        />
        {errors.firstName && (
          <p id="firstName-error" role="alert" className="text-sm text-red-600">
            {errors.firstName.message}
          </p>
        )}
      </div>
      <div className="flex flex-col gap-2">
        <label htmlFor="lastName" className="text-sm font-medium text-slate-700">
          Last name
        </label>
        <input
          id="lastName"
          autoComplete="family-name"
          {...register("lastName")}
          aria-invalid={!!errors.lastName}
          aria-describedby={errors.lastName ? "lastName-error" : undefined}
          className="rounded-lg border border-slate-300 px-3 py-2.5 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20"
          placeholder="e.g. Rivera"
        />
        {errors.lastName && (
          <p id="lastName-error" role="alert" className="text-sm text-red-600">
            {errors.lastName.message}
          </p>
        )}
      </div>
      <button
        type="submit"
        className="rounded-lg bg-blue-700 px-4 py-3 font-semibold text-white transition-colors hover:bg-blue-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-700 focus-visible:ring-offset-2"
      >
        Save player
      </button>
    </form>
  );
};

export default CreatePlayerForm;
