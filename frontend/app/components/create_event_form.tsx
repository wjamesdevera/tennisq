"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { Controller, useForm } from "react-hook-form";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import * as z from "zod";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs";

const CreateEventFormSchema = z.object({
  title: z.string().min(1, { message: "Title is required" }),
  description: z.string().optional(),
  date: z
    .string()
    .min(1, { message: "Date is required" })
    .refine((value) => dayjs(value).isValid(), { message: "Date is required" })
    .transform((value) => dayjs(value).format("YYYY-MM-DD")),
  maxPlayers: z.coerce
    .number()
    .int()
    .positive({ message: "Max players must be a positive integer" })
    .gte(2, { message: "Max players must be greater than or equal to 2" })
    .lte(50, { message: "Max players must be less than or equal to 50" })
    .optional(),
});

type CreateEventFormInput = z.input<typeof CreateEventFormSchema>;
type CreateEventFormOutput = z.output<typeof CreateEventFormSchema>;

const CreateEventForm: React.FC = () => {
  const onSubmit = (data: CreateEventFormOutput) => {
    console.log(data);
  };

  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateEventFormInput, undefined, CreateEventFormOutput>({
    resolver: zodResolver(CreateEventFormSchema),
  });
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-4 p-2 max-w-md mx-auto"
      >
        <TextField
          label="Title"
          {...register("title")}
          error={!!errors.title}
          helperText={errors.title?.message}
        />
        <TextField
          label="Description"
          {...register("description")}
          error={!!errors.description}
          helperText={errors.description?.message}
        />

        <Controller
          name="date"
          control={control}
          render={({ field }) => (
            <DatePicker
              label="Date"
              value={field.value ? dayjs(field.value) : null}
              onChange={(newValue) => {
                field.onChange(newValue ? newValue.format("YYYY-MM-DD") : "");
              }}
            />
          )}
        />
        {errors?.date && <p>{errors.date.message}</p>}

        <TextField
          label="Max Players"
          {...register("maxPlayers")}
          error={!!errors.maxPlayers}
          helperText={errors.maxPlayers?.message}
        />
        <Button variant="contained" type="submit">
          Create Event
        </Button>
      </form>
    </LocalizationProvider>
  );
};

export default CreateEventForm;
